# AnonReview - Flask File Upload App
# Team 3: HomeworkBusters

import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, g, send_from_directory, url_for, flash, redirect
from forms import LoginForm, RegistrationForm
from werkzeug.utils import secure_filename
from Constants import *

#reads from the .env file (should be in root of LOCAL repo)
load_dotenv()

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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


def allowed_file(filename):
    '''
    Check if the file has an allowed extension.
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    '''
    Connects to db, or returns active db if already connected
    '''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    '''
    Closes connection to db
    '''
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    '''
    Used to query DB
    @param query The sqlite3 query for the database
    @param args A list of arguments to be used in query - replaces ? in query
    @param one Bool for returning one value or not
    @return list with query result
    '''
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index():
    '''
    Basic landing page for project
    '''
    return render_template("index.html")

#route for login page, renders login.html by matching form to LoginForm
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = query_db('SELECT * FROM users WHERE username = ?', [form.user_name.data], one = False)
        pswd = query_db('SELECT * FROM users WHERE password_hash = ?', [form.password.data], one = False)

        #make sure request method is POST
        if user == None or pswd == None:
            #flash message and redirect to login
            return redirect(url_for("login"), form=form, invalid_login=True)
    
        else:
            #send user to dashboard
            return render_template("login.html", form=form, log_in_user=False)


    
    return render_template("login.html", form=form, log_in_user=False)

#route for registration page, renders registration.html by matching form to RegistrationForm
@app.route('/register')
def register():
    return render_template("register.html", form=RegistrationForm())

@app.route('/upload')
def upload():
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Upload File</title>
        <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
    </head>
    <body>
        <div class="container">
            <h1>AnonReview File Upload</h1>

            <form method="POST" action="{url_for('upload_file')}" enctype="multipart/form-data">
                <input type="file" name="file" />
                <br><br>
                <input type="submit" value="Upload" />
            </form>

            <br>
            <a href="{url_for('index')}">Back to Home</a>
        </div>
    </body>
    </html>
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
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    

    ##  warning: THIS NEEDS TO CHANGE WHEN DATA BASE 
    if FUNCTIONAL_DATABASE_PUSHED == 1:
        #  Save metadata to DB
        db = get_db()
        db.execute(
            "INSERT INTO files (filename, filepath) VALUES (?, ?)",
            (filename, filepath)
        )
        db.commit()
    else:
        print("File saved to server, but database interactions not implemented yet.")
        file.save(filepath)

    return f'''
        <!doctype html>
        <html>
        <head>
            <title>Upload Success</title>
            <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
        </head>
        <body>
            <div class="container">
                <h2>File Uploaded Successfully!</h2>
                <p>Filename: {filename}</p>
                <a href="{url_for('list_files')}">View Uploaded Files</a>
                <br><br>
                <a href="{url_for('upload')}">Upload Another File</a>
            </div>
        </body>
        </html>
        '''

@app.route('/files/<int:file_id>')
def get_file(file_id):

    # DB mode
    if FUNCTIONAL_DATABASE_PUSHED == 1:
        row = query_db(
            "SELECT filename FROM files WHERE id = ?",
            (file_id,),
            one=True
        )

        if not row:
            return "File not found in database", 404

        filename = row[0]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if os.path.exists(filepath):
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

        return "File missing on disk", 404

    # Dev fallback mode (no DB)
    else:
        files = sorted(os.listdir(app.config['UPLOAD_FOLDER']))

        if 0 <= file_id - 1 < len(files):
            filename = files[file_id - 1]
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

        return "File not found", 404

    

@app.route('/files')
def list_files():

    html = f'''
    <!doctype html>
    <html>
    <head>
        <title>Uploaded Files</title>
        <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
    </head>
    <body>
    <div class="container">
    <h1>Uploaded Files</h1>
    <ul>
    '''

    # DB mode
    if FUNCTIONAL_DATABASE_PUSHED == 1:
        rows = query_db("SELECT id, filename FROM files")

        for file_id, filename in rows:
            html += f'<li><a href="{url_for("get_file", file_id=file_id)}">{filename}</a></li>'

    # Dev mode
    else:
        files = sorted(os.listdir(app.config['UPLOAD_FOLDER']))

        for index, filename in enumerate(files, start=1):
            html += f'<li><a href="{url_for("get_file", file_id=index)}">{filename}</a></li>'

    html += f'''
    </ul>
    <br>
    <a href="{url_for('upload')}">Upload Another File</a>
    <br><br>
    <a href="{url_for('index')}">Back to Home</a>
    </div>
    </body>
    </html>
    '''

    return html

@app.route('/view/<filename>')
def view_file(filename):

    safe_name = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)

    if not os.path.exists(filepath):
        return "File not found", 404

    # If text file → display content
    if safe_name.endswith(('.txt', '.py')):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        return f'''
            <!doctype html>
            <html>
            <head>
                <title>Viewing {safe_name}</title>
                <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
            </head>
            <body>
                <div class="container">
                    <h2>Viewing: {safe_name}</h2>
                    <pre>{content}</pre>
                    <br>
                    <a href="{url_for('list_files')}">Back to File List</a>
                </div>
            </body>
            </html>
            '''

    # If image or pdf → render directly
    return send_from_directory(app.config['UPLOAD_FOLDER'], safe_name)

@app.route('/categories', methods=['POST', 'GET'])
def categories():
    data = query_db('SELECT * FROM categories')
    return render_template("categories.html", data=data) 

    
if __name__ == '__main__':
    print("Starting AnonReview upload server local host")
    app.run(debug=True)
