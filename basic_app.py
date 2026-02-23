# AnonReview - Flask File Upload App
# Team 3: HomeworkBusters

import os
import sqlite3
from flask import Flask, request, jsonify, render_template, g
from Constants import *

app = Flask(__name__)

# Define allowed file extensions based on flags
ALLOWED_EXTENSIONS = {}
if FLAG__FILE_EXTENSION_PY_TXT == 1:
    ALLOWED_EXTENSIONS = {'txt', 'py'}
elif FLAG__FILE_EXTENSION_PY_TXT_PDF_IMG == 1:
    ALLOWED_EXTENSIONS = {'txt', 'py', 'pdf', 'png', 'jpg', 'jpeg'}

# This can redirect to a database or cloud storage in a real implementation
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

def allowed_file(filename):
    '''
    Check if the file has an allowed extension.
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    '''
    Returns db
    '''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    '''
    Basic landing page for project
    '''
    return render_template("index.html")


@app.route('/upload')
def upload():
    '''
    Simple HTML form for file upload.
    '''
    return '''
    <h1>AnonReview File Upload</h1>
    <form method="POST" action="/upload_file" enctype="multipart/form-data">
        <input type="file" name="file" />
        <input type="submit" value="Upload" />
    </form>
    '''

@app.route('/upload_file', methods=['POST'])
def upload_file():
    '''
    Handle file upload and save it to the server.
    '''
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']

    if file.filename == '' or file.filename is None:
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    return jsonify({
        'message': 'File uploaded successfully!',
        'filename': file.filename,
        'saved_to': filepath
    }), 200


@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({'uploaded_files': files})


@app.route('/database', methods=['POST', 'GET'])
def database():
    if query_db('SELECT body FROM comments'):
        return "Database Connected"
    else:
        return "Database did not connect"

    
if __name__ == '__main__':
    print("Starting AnonReview upload server local host")
    app.run(debug=True)
