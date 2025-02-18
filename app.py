from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
import os
from utils.sketch_generator import apply_sketch
from utils.object_detection import detect_objects
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload an image (png, jpg, jpeg, gif)'}), 400

        # Clean filename to prevent security issues
        filename = os.path.basename(file.filename)
        
        # Save original image
        original_filename = f'original_{filename}'
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        file.save(original_path)

        try:
            # Process sketch version
            sketch_filename = f'sketch_{filename}'
            sketch_path = os.path.join(app.config['RESULT_FOLDER'], sketch_filename)
            apply_sketch(original_path, sketch_path)

            # Process detection version
            detect_filename = f'detect_{filename}'
            detect_path = os.path.join(app.config['RESULT_FOLDER'], detect_filename)
            detect_objects(original_path, detect_path)

            # Copy original to results folder
            shutil.copy2(original_path, os.path.join(app.config['RESULT_FOLDER'], original_filename))

            # Return result page
            return render_template('result.html', 
                                sketch_image=sketch_filename,
                                detect_image=detect_filename)
                                
        except Exception as e:
            # Clean up files in case of processing error
            if os.path.exists(original_path):
                os.remove(original_path)
            if os.path.exists(sketch_path):
                os.remove(sketch_path)
            if os.path.exists(detect_path):
                os.remove(detect_path)
            raise e

    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    try:
        # Validate filename to prevent directory traversal
        if not os.path.basename(filename) == filename:
            return "Invalid filename", 400
            
        if not os.path.exists(os.path.join(app.config['RESULT_FOLDER'], filename)):
            return "File not found", 404
            
        return send_from_directory(app.config['RESULT_FOLDER'], 
                                 filename, 
                                 as_attachment=True)
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return str(e), 500

# Error handlers
@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File is too large. Maximum size is 16MB'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'An internal server error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)