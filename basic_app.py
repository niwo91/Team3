# AnonReview - Flask File Upload App
# Team 3: HomeworkBusters
import os
import sqlite3
from dotenv import load_dotenv

from flask import Flask, request, jsonify, render_template, g, send_from_directory, url_for, redirect, session
from forms import LoginForm, RegistrationForm
from werkzeug.utils import secure_filename
from Constants import *
from anonymizer import anon_name

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
    #handles form validation, makes sure request is POST
    if form.validate_on_submit():
        user = query_db('SELECT * FROM users WHERE username = ? AND password_hash = ?', [form.user_name.data, form.password.data], one=True)

        if user == None:
            return render_template('login.html', form=form, invalid_login=True)

        else:
            return redirect("/dashboard")

    return render_template('login.html', form=form, invalid_login=False)

#route for registration page, renders registration.html by matching form to RegistrationForm
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    db = get_db()

    if form.validate_on_submit():

        existing_user = query_db('SELECT * FROM users WHERE username = ? OR email = ?', [form.user_name.data, form.email.data], one=True)

        if existing_user == None:
            query_db('INSERT INTO users (username, email, password_hash, role) ' \
            'VALUES (?, ?, ?, ?)', [form.user_name.data, form.email.data, form.password.data, form.role.data])
            db.commit()
            
            return redirect("/login")
        
        else:
            return render_template("register.html", form=form, already_exists = True)
           
    return render_template("register.html", form=form, already_exists = False)

############
## I think we can get rid of the routes below until we get to the next comment block like this
############
@app.route('/upload')
def upload():
    ## May be replaced with /create_post route
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
    ## We can get rid of this one too
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

    # SAVE FILE TO DISK (this was missing)
    file.save(filepath)

    db = get_db()

    db.execute("""
        INSERT INTO posts
        (user_id, title, body, attachment_path, attachment_type)
        VALUES (?, ?, ?, ?, ?)
    """, (
        1,                    # temporary user id
        filename,
        "Uploaded file",
        filename,             # store filename NOT full path
        filename.split('.')[-1]
    ))

    db.commit()

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

@app.route('/files/<int:post_id>')
def get_file(post_id):

    row = query_db(
        "SELECT attachment_path FROM posts WHERE post_id = ?",
        (post_id,),
        one=True
    )

    if not row:
        return "File not found in database", 404

    filename = row["attachment_path"]
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(filepath):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return "File missing on disk", 404  

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

    rows = query_db("SELECT attachment_path FROM posts")

    for row in rows:
        filename = row["attachment_path"]

        # skip broken rows
        if not filename:
            continue

        html += f'<li><a href="{url_for("view_file", filename=filename)}">{filename}</a></li>'

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

    post_comments = query_db(
        'SELECT body FROM comments WHERE post_id = (SELECT post_id FROM posts WHERE attachment_path = ?)',
        (safe_name,)
    )

    # text file display
    if safe_name.endswith(('.txt', '.py')):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()

        return render_template(
            "view_file.html",
            filename=safe_name,
            lines=content,
            comments=post_comments
        )

    # image/pdf direct render
    return send_from_directory(app.config['UPLOAD_FOLDER'], safe_name)

################
## I think we can delete the routes above
################

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        ## Uncomment below when we have user_id sessions working
        #user_id = session.get('user_id')
        title = request.form['title']
        body = request.form['body']
        category_id = request.form.get('category_id')
        attachment_path = request.files['file']
        attachment_type = None
        filename = None
        

        # Check file validity
        # Attachment not required
        if attachment_path.filename != None and attachment_path.filename != '':
            if not allowed_file(attachment_path.filename):
                return jsonify({'error': f'File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}'}), 400
            else:
                filename = secure_filename(attachment_path.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                attachment_path.save(filepath)
                attachment_type = filename.split('.')[-1]

        db = get_db()

        # Insert post without anon_name first
        cursor = db.execute(
            """
            INSERT INTO posts (user_id, category_id, title, body, attachment_path, attachment_type)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            # Replace 1 with user_id when we have user id sessions working
            (1, category_id, title, body, filename, attachment_type)
        )
        post_id = cursor.lastrowid

        # Generate pseudonym
        ## Update 1 with user id when user sessions are working
        pseudonym = anon_name(1, post_id)

        # Update post with anon_name
        db.execute(
            "UPDATE posts SET anon_name = ? WHERE post_id = ?",
            (pseudonym, post_id)
        )
        db.commit()

        return redirect(url_for('view_post', post_id=post_id))

    categories = query_db("SELECT * FROM categories")
    return render_template("create_post.html", categories=categories)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = query_db(
        "SELECT * FROM posts WHERE post_id = ?",
        (post_id,),
        one=True
    )
    comments = query_db(
        "SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC",
        (post_id,)
    )
    filename = post[5]
        
    # No functionality for pdf or images yet
    if filename is not None:
        safe_name = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
        if safe_name.endswith(('.txt', '.py')):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.readlines()
            return render_template("view_post.html", post=post, comments=comments, lines=content) 

    return render_template("view_post.html", post=post, comments=comments, lines=None)

@app.route('/dashboard')
def dashboard():
    posts = query_db(
        "SELECT * FROM posts ORDER BY created_at DESC LIMIT 20"
    )
    return render_template("dashboard.html", posts=posts)

@app.route('/submit_form', methods=["POST"])
def submit_form():
    comment = request.form.get("comment")
    filename = request.form.get("filename")
    ## Will need to be updated to allow for user ids, etc with database
    db = get_db()
    query_db(
            'INSERT INTO comments (post_id, user_id, body, comment_anchor, created_at) VALUES (?, ?, ?, ?, ?)', 
            [2, 1, comment, 'a', '1/1/2001'], 
            one=True)
    db.commit()
    return view_file(filename)

@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    #Update User_id when we have sessions
    user_id = 1 # Update to session.get('user_id')
    body = request.form['body']

    db = get_db()

    pseudonym = anon_name(user_id, post_id)

    db.execute(
        """
        INSERT INTO comments (post_id, user_id, body, anon_name)
        VALUES (?, ?, ?, ?)
        """,
        (post_id, 1, body, pseudonym)# Update USer id when we have sessions
    )
    db.commit()

    return redirect(url_for('view_post', post_id=post_id))
    
if __name__ == '__main__':
    print("Starting AnonReview upload server local host")
    app.run(debug=True)
