from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import subprocess
import os

app = Flask(__name__)

# Enable CORS for all domains (or specify a specific domain if you prefer)
CORS(app)

# Define the upload folder to be 'user-inputs'
UPLOAD_FOLDER = 'user-inputs'  # You can use a relative path or absolute path
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
    # Check if a file was submitted in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file to the user-inputs folder
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print("Hello, World!")
    file.save(file_path)

    # After saving the file, run the external script
    try:
        # Run the external tester script using subprocess
        result = subprocess.run(
            ['python3', 'external-tester.py', file_path],  # Path to your script and the saved file
            capture_output=True,  # Capture output so you can log it or return it
            text=True
        )

        print("Result file path: ", result)
        print("File path: ", file_path)

        # Print the output of the script (you can also use result.stdout for logging or debugging)
        print("Script Output:", result.stdout)
        print("Script Error (if any):", result.stderr)
        print(result.returncode)

        # You can send a response back based on the output of the script
        if result.returncode == 0:
            # Return the output of the script to the frontend
            print("Result: ", result.stdout)
            return jsonify({"message": result.stdout.strip()}), 200  # Strip to remove any extra newline
        else:
            return jsonify({"error": f"External script failed: {result.stderr}"}), 500

    except Exception as e:
        return jsonify({"error": f"Error running external script: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)