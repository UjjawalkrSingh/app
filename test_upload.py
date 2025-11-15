#!/usr/bin/env python3
"""
Test script to upload sample traffic videos to the AI Traffic Management System
"""

import requests
import os
import time

def test_upload():
    # Backend URL
    url = 'http://127.0.0.1:5000/upload'
    
    # Sample video files
    video_files = [
        '/Users/karan/Documents/infothon1/Infothon-1/backend/uploads/sample_traffic_north.mp4',
        '/Users/karan/Documents/infothon1/Infothon-1/backend/uploads/sample_traffic_south.mp4', 
        '/Users/karan/Documents/infothon1/Infothon-1/backend/uploads/sample_traffic_east.mp4',
        '/Users/karan/Documents/infothon1/Infothon-1/backend/uploads/sample_traffic_west.mp4'
    ]
    
    print("🚦 AI Traffic Management System - Test Upload")
    print("=" * 50)
    
    # Check if all video files exist
    print("📁 Checking video files...")
    for i, video_file in enumerate(video_files, 1):
        if os.path.exists(video_file):
            file_size = os.path.getsize(video_file) / (1024 * 1024)  # MB
            print(f"✅ Video {i}: {os.path.basename(video_file)} ({file_size:.1f} MB)")
        else:
            print(f"❌ Video {i}: {video_file} - File not found!")
            return
    
    print("\n📤 Uploading videos to backend...")
    
    # Prepare files for upload
    files = []
    try:
        for video_file in video_files:
            files.append(('videos', (os.path.basename(video_file), open(video_file, 'rb'), 'video/mp4')))
        
        print("⏳ Processing videos (this may take a few minutes)...")
        start_time = time.time()
        
        # Make the request
        response = requests.post(url, files=files, timeout=300)  # 5 minute timeout
        
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS! Processing completed in {processing_time:.1f} seconds")
            print("\n🚦 OPTIMIZED TRAFFIC LIGHT TIMINGS:")
            print("=" * 40)
            print(f"🔵 North Direction: {result['north']} seconds")
            print(f"🔴 South Direction: {result['south']} seconds") 
            print(f"🟢 East Direction:  {result['east']} seconds")
            print(f"🟡 West Direction:  {result['west']} seconds")
            print("=" * 40)
            print("\n💡 These timings are optimized based on:")
            print("   • Vehicle count analysis using YOLOv4")
            print("   • Genetic algorithm optimization")
            print("   • Traffic flow patterns")
            
        else:
            print(f"\n❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend server")
        print("   Make sure the Flask server is running on http://127.0.0.1:5000")
        
    except requests.exceptions.Timeout:
        print("\n⏰ Error: Request timed out")
        print("   Video processing is taking longer than expected")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
    finally:
        # Close all file handles
        for file_tuple in files:
            if len(file_tuple) > 1 and hasattr(file_tuple[1][1], 'close'):
                file_tuple[1][1].close()

if __name__ == "__main__":
    test_upload()