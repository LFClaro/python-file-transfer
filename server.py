import os
from flask import Flask, json, request
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
DOWNLOAD_FOLDER = os.path.join(path, 'downloads/newUploads/')

# Make directory for downloads if it doesn't exist
if not os.path.isdir(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)
    print(f'{DOWNLOAD_FOLDER} created')

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = set(['mp4', 'xml'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello():
    return 'Hello World! API is running'


@app.route('/uploads', methods=['PUT'])
def upload_file():
    if request.method == 'PUT':
        if 'files' not in request.files:
            return "No files found", 400

        files = request.files.getlist('files')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['DOWNLOAD_FOLDER'], filename))
                print(f'{file.filename} DOWNLOADED')

        return json.dumps({"success": True}), 201

@app.route('/delete/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        url = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        os.remove(url)
        print(f'{filename} DELETED')
        return json.dumps({"success": True}), 200
    except FileNotFoundError as e:
        return e.args, 204


if __name__ == '__main__':
    app.run(host="localhost", port=8081, threaded = True) 