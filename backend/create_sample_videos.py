import cv2
import numpy as np
import os

def create_sample_traffic_video(filename, duration=10, fps=30):
    """Create a sample traffic video with moving rectangles simulating cars"""
    
    # Video properties
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Create VideoWriter object
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    # Generate frames
    total_frames = duration * fps
    
    for frame_num in range(total_frames):
        # Create black background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Draw road lines
        cv2.line(frame, (0, height//2), (width, height//2), (255, 255, 255), 2)  # Horizontal road
        cv2.line(frame, (width//2, 0), (width//2, height), (255, 255, 255), 2)   # Vertical road
        
        # Simulate moving cars (rectangles)
        num_cars = np.random.randint(1, 6)  # Random number of cars (1-5)
        
        for i in range(num_cars):
            # Random car properties
            car_width, car_height = 40, 20
            
            # Different movement patterns for different directions
            if i % 4 == 0:  # Moving right
                x = (frame_num * 3 + i * 50) % width
                y = height//2 - 50 + i * 10
            elif i % 4 == 1:  # Moving left
                x = width - ((frame_num * 2 + i * 60) % width)
                y = height//2 + 30 + i * 10
            elif i % 4 == 2:  # Moving down
                x = width//2 - 50 + i * 15
                y = (frame_num * 2 + i * 40) % height
            else:  # Moving up
                x = width//2 + 30 + i * 15
                y = height - ((frame_num * 3 + i * 30) % height)
            
            # Draw car (rectangle)
            color = (0, 255, 0) if i % 2 == 0 else (0, 0, 255)  # Green or Red cars
            cv2.rectangle(frame, (int(x), int(y)), (int(x + car_width), int(y + car_height)), color, -1)
        
        # Add some noise/texture to make it more realistic
        noise = np.random.randint(0, 30, (height, width, 3), dtype=np.uint8)
        frame = cv2.add(frame, noise)
        
        # Write frame
        out.write(frame)
    
    # Release everything
    out.release()
    print(f"Created sample video: {filename}")

def main():
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    
    # Create 4 sample videos representing different intersection directions
    directions = ['north', 'south', 'east', 'west']
    
    for i, direction in enumerate(directions):
        filename = f'uploads/sample_traffic_{direction}.mp4'
        create_sample_traffic_video(filename, duration=15, fps=20)
    
    print("✅ Created 4 sample traffic videos in the uploads folder!")
    print("You can now test the application with these videos.")

if __name__ == "__main__":
    main()