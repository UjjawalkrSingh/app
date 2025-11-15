from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from yolov4 import detect_cars
from algo import optimize_traffic

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_files():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    uploads_dir = os.path.join(script_dir, 'uploads')
    
    files = request.files.getlist('videos')
    if len(files) != 4:
        return jsonify({'error': 'Please upload exactly 4 videos'}), 400

    video_paths = []
    for i, file in enumerate(files):
        video_path = os.path.join(uploads_dir, f'video_{i}.mp4')
        file.save(video_path)
        video_paths.append(video_path)

    num_cars_list = []
    for video_file in video_paths:
        num_cars = detect_cars(video_file)
        num_cars_list.append(num_cars)

    result = optimize_traffic(num_cars_list)

    return jsonify(result)

if __name__ == '__main__':
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    uploads_dir = os.path.join(script_dir, 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    app.run(debug=True)
