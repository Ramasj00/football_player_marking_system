from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
from model_test import MarkPlayerModel
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Configure upload folder paths
UPLOAD_FOLDER = 'uploads'
PROCESSED_UPLOADS_FOLDER = 'processed_uploads'
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_UPLOADS_FOLDER, exist_ok=True)

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def process_video(input_path, output_path):
    try:
        model = MarkPlayerModel(input_path, output_path)
        model.predict_player()
    except Exception as e:
        app.logger.error(f"Error processing video {input_path}: {e}")
        raise

@app.route('/processed_videos/<filename>')
def get_processed_video(filename):
    return send_from_directory('processed_uploads', filename)

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400
    
    video = request.files['video']
    
    if video.filename == '':
        return jsonify({"error": "No video file selected"}), 400
    
    if not allowed_video_file(video.filename):
        return jsonify({
            "error": "Invalid video format. Allowed formats are: " +
            ", ".join(ALLOWED_VIDEO_EXTENSIONS)
        }), 400

    try:
        # Generate a unique filename for the input file
        unique_filename = f"{uuid.uuid4()}_{video.filename}"
        input_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        video.save(input_path)

        # Create the output filename with "processed_" prefix and the '_tracked' suffix before the file extension.
        file_base, file_ext = os.path.splitext(unique_filename)
        output_filename = f"processed_{file_base}_tracked.mp4"
        output_path = os.path.join(PROCESSED_UPLOADS_FOLDER, output_filename)
        
        # Process video synchronously
        process_video(input_path, output_path)
        
        return jsonify({
            "message": "Video processed successfully",
            "input_filename": unique_filename,
            "output_filename": os.path.abspath(output_path)
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error occurred while processing video: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)