# AnonReview - Flask File Upload App
# Team 3: HomeworkBusters
import os
import sqlite3
from dotenv import load_dotenv
import time

from flask import Flask, request, jsonify, render_template, g, send_from_directory, url_for, redirect, session, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from passlib.hash import pbkdf2_sha512
from datetime import timedelta
from forms import LoginForm, RegistrationForm
from werkzeug.utils import secure_filename
from Constants import *
from anonymizer import anon_name

import docx
from bs4 import BeautifulSoup
import PyPDF2

#reads from the .env file (should be in root of LOCAL repo)
load_dotenv()

app = Flask(__name__)

# Define allowed file extensions based on flags
ALLOWED_EXTENSIONS = {}
if FLAG__FILE_EXTENSION_PY_TXT == 1:
    ALLOWED_EXTENSIONS = {
    'txt', 'py',
    'pdf', 'html',
    'doc', 'docx'
}
elif FLAG__FILE_EXTENSION_PY_TXT_PDF_IMG == 1:
    ALLOWED_EXTENSIONS = {'txt', 'py', 'pdf', 'png', 'jpg', 'jpeg'}

# This can redirect to a database or cloud storage in a real implementation
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60) #user session times out after an hour if no requests made
app.config['SESSION_REFRESH_EACH_REQUEST'] = True #timer is reset by requests


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

def init_categories():
    db = get_db()

    db.execute("INSERT INTO categories (name) VALUES (?)", ("Homework",))
    db.execute("INSERT INTO categories (name) VALUES (?)", ("Project",))
    db.execute("INSERT INTO categories (name) VALUES (?)", ("Exam Prep",))
    db.execute("INSERT INTO categories (name) VALUES (?)", ("General",))
    db.execute("INSERT INTO categories (name) VALUES (?)", ("Code Review",))

    db.commit()

    return "Categories initialized!" 

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

def blobify(file):
    """
    @param file to turn into a binary blob
    @return binary blob of file
    """
    data = 0
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_file')
    file.save(filepath)
    with open(filepath, 'rb') as file:
        data = file.read()
    os.remove(filepath)
    return data


def unblobify(binary, file_type):
    """
    @param binary of file
    @return file for display
    """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_file')

    with open(filepath, "wb") as f:
        f.write(binary)

    content = []

    # TEXT / CODE line-by-line
    if file_type in ['txt', 'py']:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()

    # HTML treat like text (line-by-line)
    elif file_type == 'html':
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, "html.parser")
            content = soup.prettify().split('\n')

    # PDF extract text
    elif file_type == 'pdf':
        reader = PyPDF2.PdfReader(filepath)
        for page in reader.pages:
            content.extend(page.extract_text().split('\n'))

    # DOCX → paragraphs
    elif file_type == 'docx':
        doc = docx.Document(filepath)
        content = [p.text for p in doc.paragraphs]

    # DOC (old)  fallback (no good parser)
    elif file_type == 'doc':
        content = ["Preview not supported. Download file instead."]

    os.remove(filepath)
    return content


#database method to check whether user should be logged in
def check_user(username, password):

    user = query_db(
        "SELECT * FROM users WHERE username = ?",
        (username,),
        one=True
    )

    if not user:
        return None, False, False

    valid_password = pbkdf2_sha512.verify(password, user["password_hash"])
    is_active = user["is_active"] == 1

    return [user["user_id"], user["username"], user["role"]], valid_password, is_active

#database method to check whether selected username and password already exist
def check_registration(username, email):

    existing_username = query_db(
        "SELECT 1 FROM users WHERE username = ?",
        (username,),
        one=True
    )

    existing_email = query_db(
        "SELECT 1 FROM users WHERE email = ?",
        (email,),
        one=True
    )

    return bool(existing_username), bool(existing_email)


#database method to add new user to users tables
def register_user(username, email, password, role):
    
    db = get_db()
    hashed_password = pbkdf2_sha512.hash(password)

    db.execute(
        """
        INSERT INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
        """,
        (username, email, hashed_password, role)
    )
    db.commit()
    

#connects the app and the Flask-Login extension
login_manager = LoginManager()
login_manager.init_app(app)

#User class, object can be made with data from database. Inherits required methods from UserMixin
class User(UserMixin):
    def __init__(self, id, name, role, active):
        
        self.id = id
        self.name = name
        self.role = role
        self.active = active

# Load moderation category ID safely
with app.app_context():
    row = query_db(
        "SELECT category_id FROM categories WHERE name = 'Reported Items'",
        one=True
    )
    REPORTED_CATEGORY_ID = row['category_id'] if row else None

#login manager reloads user ID stored in session
@login_manager.user_loader
def load_user(user_id):
    user_row = query_db('SELECT * FROM users WHERE user_id = ?', [user_id], one=True)

    if user_row == None:
        return None
    
    user = User(user_row[0], user_row[1], user_row[4], user_row[5])
    return user


@app.route('/')
def index():
    '''
    Basic landing page for project
    '''
    return render_template("index.html")



#route for login page
@app.route('/login', methods=['POST', 'GET'])
def login():

    form = LoginForm()

    #if user is already logged in redirect them to their dashboard
    if current_user.is_authenticated:
        return redirect("/dashboard")

    #handles form validation, makes sure request is POST
    if form.validate_on_submit():
        user_data = check_user(form.user_name.data, form.password.data)
        user_row = user_data[0]
        valid_credentials = (user_row != None and user_data[1] == True)
        user_active = user_data[2]

        if valid_credentials == False:
            return render_template('login.html', form=form, invalid_login=True)
        
        
        elif user_active == False:
            return render_template('login.html', form=form, not_active=True)

        #if credentials are valid and user is active, log in
        else:
            user_obj = User(user_row[0], user_row[1], user_row[2], user_active) #create User object
            login_user(user_obj)
            session["user_id"] = user_row[0]
            session["role"] = user_row[2] 
            session.permanent = True #session is permanent so that config can handle timeouts
            return redirect("/dashboard")

    return render_template('login.html', form=form, invalid_login=False)


#route for registration page
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    db = get_db()

    #if user is already logged in redirect them to dashboard
    if current_user.is_authenticated:
        return redirect("/dashboard")

    if form.validate_on_submit():

        registration_data = check_registration(form.user_name.data, form.email.data)

        #if username and email do not exist, and password check matches password, register the user and redirect to login
        if registration_data == (False, False):

            if form.password.data != form.password_check.data:
                return render_template("register.html", form=form, different_passwords = True)
            
            register_user(form.user_name.data, form.email.data, form.password.data, form.role.data)
            
            flash("Registration successful! Please log in.") #inform user that registration was successful
            return redirect("/login")
        
        #if username exists, inform user and do not register
        elif registration_data[0] != False:
            return render_template("register.html", form=form, username_already_exists = True)
        
        #if email exists inform user and do not register
        elif registration_data[1] != False:
            return render_template("register.html", form=form, email_already_exists = True)
           
    return render_template("register.html", form=form, already_exists = False)

#user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


#sends user to index page if session times out
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/")

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):

    db = get_db()

    # get file name from DB
    row = query_db(
        "SELECT post_id, user_id FROM posts WHERE post_id = ?",
        (post_id,),
        one=True
    )

    if not row:
        return "Post not found", 404
    

    # Permission check
    user = {
        'user_id': current_user.id,
        'role': current_user.role    }
    is_owner = (user['user_id'] == row['user_id'])
    is_admin = (user['role'] == 'admin')
    is_mod = (user['role'] == 'moderator')

    if not (is_owner or is_admin or is_mod):
        return "Forbidden", 403

    # delete comments related to the post
    db.execute(
        "DELETE FROM comments WHERE post_id = ?",
        (post_id,)
    )

    # delete the post itself
    db.execute(
        "DELETE FROM posts WHERE post_id = ?",
        (post_id,)
    )

    db.commit()

    return redirect(url_for('dashboard'))

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():

    # --- CATEGORY FILTERING (for GET and POST) ---
    if current_user.role in ('admin', 'moderator'):
        categories = query_db("SELECT * FROM categories")
    else:
        categories = query_db(
            "SELECT * FROM categories WHERE name != 'Reported Items'"
        )

    # If categories table is empty, initialize it
    if not categories:
        init_categories()

    # --- HANDLE POST REQUEST ---
    if request.method == 'POST':
        user_id = current_user.id
        title = request.form['title']
        body = request.form['body']
        category_id = request.form.get('category_id')

        if current_user.role not in ('admin', 'moderator') and int(category_id) == REPORTED_CATEGORY_ID:
            return "Unauthorized", 403

        attachment = request.files['file']
        attachment_type = None
        filename = None
        attachment_blob = None

        if attachment and attachment.filename:
            if not allowed_file(attachment.filename):
                return jsonify({'error': f'File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}'}), 400

            filename = secure_filename(attachment.filename)
            attachment_blob = blobify(attachment)
            attachment_type = filename.split('.')[-1]

        db = get_db()

        cursor = db.execute(
            """
            INSERT INTO posts (user_id, category_id, title, body, attachment_name, attachment_blob, attachment_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, category_id, title, body, filename, attachment_blob, attachment_type)
        )
        post_id = cursor.lastrowid

        pseudonym = anon_name(1, post_id)

        db.execute(
            "UPDATE posts SET anon_name = ? WHERE post_id = ?",
            (pseudonym, post_id)
        )
        db.commit()

        return redirect(url_for('view_post', post_id=post_id))

    return render_template("create_post.html", categories=categories)


@app.route('/post/<int:post_id>')
@login_required
def view_post(post_id):
    post = query_db(
        "SELECT * FROM posts WHERE post_id = ?",
        (post_id,),
        one=True
    )

    if not post:
        return "Post not found", 404

    comments = query_db(
        """
        SELECT comment_id, body, anon_name, line_number, upvotes, downvotes
        FROM comments
        WHERE post_id = ?
        ORDER BY created_at ASC
        """,
        (post_id,)
    )

    # Group comments
    comments_by_line = {}
    general_comments = []

    for c in comments:
        line = c["line_number"]

        if line is not None:
            comments_by_line.setdefault(line, []).append(c)
        else:
            general_comments.append(c)

    filename = post["attachment_name"]

    # Handle file display
    if filename:
        content = unblobify(
            post["attachment_blob"],
            post["attachment_type"]
        )

        return render_template(
            "view_post.html",
            post=post,
            lines=content,
            comments_by_line=comments_by_line,
            general_comments=general_comments
        )

    return render_template(
        "view_post.html",
        post=post,
        lines=None,
        comments_by_line={},
        general_comments=general_comments
    )

@app.route('/comment/<int:comment_id>/vote', methods=['POST'])
@login_required
def vote_comment(comment_id):
    vote_type = request.form.get("vote")  # "up" or "down"
    user_id = current_user.id

    db = get_db()

    existing = query_db(
        "SELECT * FROM comment_votes WHERE user_id = ? AND comment_id = ?",
        (user_id, comment_id),
        one=True
    )

    if existing:
        return redirect(request.referrer)

    db.execute(
        "INSERT INTO comment_votes (user_id, comment_id, vote_type) VALUES (?, ?, ?)",
        (user_id, comment_id, vote_type)
    )

    if vote_type == "up":
        db.execute("UPDATE comments SET upvotes = upvotes + 1 WHERE comment_id = ?", (comment_id,))
    else:
        db.execute("UPDATE comments SET downvotes = downvotes + 1 WHERE comment_id = ?", (comment_id,))

    db.commit()

    return redirect(request.referrer)

@app.route('/dashboard')
@login_required
def dashboard():
    category_id = request.args.get('category')

    # If a category is selected
    if category_id:
        # Prevent normal users from accessing the moderation queue
        if current_user.role not in ('admin', 'moderator') and int(category_id) == REPORTED_CATEGORY_ID:
            return "Unauthorized", 403

        posts = query_db(
            "SELECT * FROM posts WHERE category_id = ? ORDER BY created_at DESC",
            (category_id,)
        )

    else:
        # No category selected
        if current_user.role in ('admin', 'moderator'):
            posts = query_db(
                "SELECT * FROM posts ORDER BY created_at DESC"
            )
        else:
            posts = query_db(
                "SELECT * FROM posts WHERE category_id != ? ORDER BY created_at DESC",
                (REPORTED_CATEGORY_ID,)
            )

    # Category list (admins/mods see all, users see all except moderation queue)
    if current_user.role in ('admin', 'moderator'):
        categories = query_db("SELECT * FROM categories")
    else:
        categories = query_db(
            "SELECT * FROM categories WHERE name != 'Reported Items'"
        )

    return render_template(
        "dashboard.html",
        posts=posts,
        categories=categories,
        selected_category=category_id
    )

@app.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    user_id = current_user.id 
    body = request.form['body']
    line_number = request.form.get('line_number')  # Optional, for text file comments

    db = get_db()

    pseudonym = anon_name(user_id, post_id)
    if line_number:
        line_number = int(line_number)
        db.execute(
            """
            INSERT INTO comments (post_id, user_id, body, anon_name, line_number)
            VALUES (?, ?, ?, ?, ?)
            """,
            (post_id, user_id, body, pseudonym, line_number) # Update USer id when we have sessions
        )
    else:
        db.execute(
            """
            INSERT INTO comments (post_id, user_id, body, anon_name)
            VALUES (?, ?, ?, ?)
            """,
            (post_id, user_id, body, pseudonym)# Update USer id when we have sessions
        )
    db.commit()

    return redirect(url_for('view_post', post_id=post_id))

@app.route('/report/post/<int:post_id>', methods=['POST'])
@login_required
def report_post(post_id):
    reason = request.form.get('reason', 'No reason provided')
    user_id = session['user_id']

    conn = get_db()

    conn.execute("""
        INSERT INTO reports (user_id, post_id, reason)
        VALUES (?, ?, ?)
    """, (user_id, post_id, reason))

    conn.execute("""
        UPDATE posts SET reported = 1, category_id = ?
        WHERE post_id = ?
    """, (REPORTED_CATEGORY_ID, post_id))

    conn.commit()
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/report/comment/<int:comment_id>', methods=['POST'])
@login_required
def report_comment(comment_id):
    reason = request.form.get('reason', 'No reason provided')
    user_id = session['user_id']

    db = get_db()

    # Insert report + mark comment
    db.execute(
        "INSERT INTO reports (user_id, comment_id, reason) VALUES (?, ?, ?)",
        (user_id, comment_id, reason)
    )
    db.execute(
        "UPDATE comments SET reported = 1 WHERE comment_id = ?",
        (comment_id,)
    )

    # Move parent post into moderation category
    post = query_db(
        "SELECT post_id FROM comments WHERE comment_id = ?",
        (comment_id,),
        one=True
    )
    if post:
        db.execute(
            "UPDATE posts SET reported = 1, category_id = ? WHERE post_id = ?",
            (REPORTED_CATEGORY_ID, post['post_id'])
        )

    db.commit()
    return redirect(request.referrer)


@app.route('/admin/reports')
@login_required
def view_reports():
    if session.get('role') not in ('admin', 'moderator'):
        return "Unauthorized", 403

    db = get_db()
    reports = db.execute("""
        SELECT r.*, u.username, p.title AS post_title, c.body AS comment_body
        FROM reports r
        LEFT JOIN users u ON r.user_id = u.user_id
        LEFT JOIN posts p ON r.post_id = p.post_id
        LEFT JOIN comments c ON r.comment_id = c.comment_id
        ORDER BY r.created_at DESC
    """).fetchall()

    return render_template('admin_reports.html', reports=reports)

@app.route('/unreport/post/<int:post_id>', methods=['POST'])
@login_required
def unreport_post(post_id):
    if current_user.role not in ('admin', 'moderator'):
        return "Unauthorized", 403

    db = get_db()

    # Move post back to a normal category (default: General)
    db.execute(
        "UPDATE posts SET reported = 0, category_id = 1 WHERE post_id = ?",
        (post_id,)
    )

    db.commit()
    return redirect(request.referrer)

@app.route('/delete/comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    if current_user.role not in ('admin', 'moderator'):
        return "Unauthorized", 403

    db = get_db()
    db.execute("DELETE FROM comments WHERE comment_id = ?", (comment_id,))
    db.commit()

    return redirect(request.referrer)

@app.route('/unreport/comment/<int:comment_id>', methods=['POST'])
@login_required
def unreport_comment(comment_id):
    if current_user.role not in ('admin', 'moderator'):
        return "Unauthorized", 403

    db = get_db()
    db.execute(
        "UPDATE comments SET reported = 0 WHERE comment_id = ?",
        (comment_id,)
    )
    db.commit()

    return redirect(request.referrer)

if __name__ == '__main__':
    print("Starting AnonReview upload server local host")
    app.run(debug=True)
