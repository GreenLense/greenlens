from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os

app = Flask(__name__)

# Enable CORS for all domains (or specify a specific domain if you prefer)
CORS(app)

# Define the upload folder to be 'user-inputs'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'user-inputs')  # You can use a relative path or absolute path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# POST endpoint for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the file to the 'user-inputs' directory
        file.save(filepath)
        
        # Print the file information (for testing purposes)
        print(f"Received file: {filename}")
        print(f"File path: {filepath}")

        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'filepath': filepath
        }), 200

    return jsonify({'error': 'File type not allowed'}), 400

# Run the Flask app on port 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)