from flask import Flask, render_template, request, send_from_directory
import os
from utils.sketch_generator import apply_sketch
from utils.object_detection import detect_objects

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return "No file uploaded!", 400
    file = request.files['file']

    if file.filename == '':
        return "No selected file!", 400

    feature = request.form.get('feature')
    if feature not in ['sketch', 'detect']:
        return "Invalid feature selected!", 400

    # Save uploaded image
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Process the image
    result_path = ''
    if feature == 'sketch':
        result_path = os.path.join(app.config['RESULT_FOLDER'], f'sketch_{file.filename}')
        apply_sketch(filepath, result_path)
    elif feature == 'detect':
        result_path = os.path.join(app.config['RESULT_FOLDER'], f'detect_{file.filename}')
        detect_objects(filepath, result_path)

    # Send the result back to the user
    return send_from_directory(app.config['RESULT_FOLDER'], os.path.basename(result_path))

if __name__ == '__main__':
    app.run(debug=True)
