# AnonReview - Flask File Upload App
# Team 3: HomeworkBusters
import os
import psycopg2
import os
from dotenv import load_dotenv
import time

from flask import Flask, request, jsonify, render_template, g, send_from_directory, url_for, redirect, session, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from passlib.hash import pbkdf2_sha512
from datetime import timedelta
from forms import LoginForm, RegistrationForm, RoleUpdateForm
from werkzeug.utils import secure_filename
from Constants import *
from anonymizer import anon_name
from methods import *

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
    curr = db.cursor()
    curr.execute("INSERT INTO categories (name) VALUES (%s)", ("Homework",))
    curr.execute("INSERT INTO categories (name) VALUES (%s)", ("Project",))
    curr.execute("INSERT INTO categories (name) VALUES (%s)", ("Exam Prep",))
    curr.execute("INSERT INTO categories (name) VALUES (%s)", ("General",))
    curr.execute("INSERT INTO categories (name) VALUES (%s)", ("Code Review",))
    curr.close()

    db.commit()

    return "Categories initialized!" 

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
def get_reported_category_id():
    row = query_db(
        "SELECT category_id FROM categories WHERE name = %s",
        ("Reported Items",),
        one=True
    )
    return row["category_id"] if row else None

#login manager reloads user ID stored in session
@login_manager.user_loader
def load_user(user_id):
    user_row = query_db('SELECT * FROM users WHERE user_id = %s', [user_id], one=True)

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
            
            register_user(form.user_name.data, form.email.data, form.password.data)
            
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
        "SELECT post_id, user_id FROM posts WHERE post_id = %s",
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

    delete_post(post_id)

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

        if current_user.role not in ('admin', 'moderator') and int(category_id) == get_reported_category_id():
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

        cursor = create_a_post(user_id, category_id, title, body, filename, attachment_blob, attachment_type)

        post_id = cursor.lastrowid

        pseudonym = anon_name(1, post_id)

        db = get_db()
        curr = db.cursor()
        curr.execute(
            "UPDATE posts SET anon_name = %s WHERE post_id = %s",
            (pseudonym, post_id)
        )
        db.commit()
        curr.close()

        return redirect(url_for('view_post', post_id=post_id))

    return render_template("create_post.html", categories=categories)


@app.route('/post/<int:post_id>')
@login_required
def view_post(post_id):
    post = get_post(post_id)

    if not post:
        return "Post not found", 404

    comments = get_comments(post_id)

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

    vote_a_comment(user_id, comment_id, vote_type)

    return redirect(request.referrer)

@app.route('/dashboard')
@login_required
def dashboard():
    category_id = request.args.get('category')

    # Load categories first
    if current_user.role in ('admin', 'moderator'):
        categories = query_db("SELECT * FROM categories")
    else:
        categories = query_db(
            "SELECT * FROM categories WHERE name != 'Reported Items'"
        )

    categories = [dict(c) for c in categories]

    # Add NEW POST flag to categories
    for cat in categories:
        new_count = query_db(
            """
            SELECT COUNT(*) AS c
            FROM posts
            WHERE category_id = %s
            AND created_at > datetime('now', '-1 day')
            """,
            (cat['category_id'],),
            one=True
        )['c']
        cat['has_new'] = new_count > 0

    # Load posts depending on category selection
    if category_id:
        if current_user.role not in ('admin', 'moderator') and int(category_id) == get_reported_category_id():
            return "Unauthorized", 403

        posts = query_db(
            "SELECT * FROM posts WHERE category_id = %s ORDER BY created_at DESC",
            (category_id,)
        )
    else:
        if current_user.role in ('admin', 'moderator'):
            posts = query_db("SELECT * FROM posts ORDER BY created_at DESC")
        else:
            posts = query_db(
                "SELECT * FROM posts WHERE category_id != %s ORDER BY created_at DESC",
                (get_reported_category_id(),)
            )

    posts = [dict(p) for p in posts]

    # Add NEW COMMENTS flag to posts
    for post in posts:
        recent_comments = query_db(
            """
            SELECT COUNT(*) AS c
            FROM comments
            WHERE post_id = %s
            AND created_at > datetime('now', '-1 day')
            """,
            (post['post_id'],),
            one=True
        )['c']

        post['has_new_comments'] = recent_comments > 0

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
        add_a_comment(post_id, user_id, body, pseudonym, line_number)
    else:
        add_a_comment(post_id, user_id, body, pseudonym)

    return redirect(url_for('view_post', post_id=post_id))

@app.route('/report/post/<int:post_id>', methods=['POST'])
@login_required
def report_post(post_id):
    reason = request.form.get('reason', 'No reason provided')
    user_id = session['user_id']

    flag_item(user_id, post_id, reason=reason, comment_id=None)

    return redirect(url_for('view_post', post_id=post_id))

@app.route('/report/comment/<int:comment_id>', methods=['POST'])
@login_required
def report_comment(comment_id):
    reason = request.form.get('reason', 'No reason provided')
    user_id = session['user_id']

    db = get_db()

    # Move parent post into moderation category
    post = query_db(
        "SELECT post_id FROM comments WHERE comment_id = %s",
        (comment_id,),
        one=True
    )

    flag_item(user_id, post[0], comment_id, reason)

    return redirect(request.referrer)


@app.route('/admin/reports')
@login_required
def view_reports():
    if session.get('role') not in ('admin', 'moderator'):
        return "Unauthorized", 403

    db = get_db()
    curr = db.cursor()
    reports = curr.execute("""
        SELECT r.*, u.username, p.title AS post_title, c.body AS comment_body
        FROM reports r
        LEFT JOIN users u ON r.user_id = u.user_id
        LEFT JOIN posts p ON r.post_id = p.post_id
        LEFT JOIN comments c ON r.comment_id = c.comment_id
        ORDER BY r.created_at DESC
    """).fetchall()
    curr.close()

    return render_template('admin_reports.html', reports=reports)

@app.route('/unreport/post/<int:post_id>', methods=['POST'])
@login_required
def unreport_post(post_id):
    if current_user.role not in ('admin', 'moderator'):
        return "Unauthorized", 403

    db = get_db()
    curr = db.cursor()

    # Move post back to a normal category (default: General)
    curr.execute(
        "UPDATE posts SET reported = 0, category_id = 1 WHERE post_id = %s",
        (post_id,)
    )
    curr.close()
    db.commit()
    return redirect(request.referrer)

@app.route('/delete/comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    if current_user.role not in ('admin', 'moderator'):
        return "Unauthorized", 403

    db = get_db()
    curr = db.cursor()
    curr.execute("DELETE FROM comments WHERE comment_id = %s", (comment_id,))
    db.commit()
    curr.close()

    return redirect(request.referrer)

@app.route('/unreport/comment/<int:comment_id>', methods=['POST'])
@login_required
def unreport_comment(comment_id):
    if current_user.role not in ('admin', 'moderator'):
        return "Unauthorized", 403

    db = get_db()
    curr = db.cursor()
    curr.execute(
        "UPDATE comments SET reported = 0 WHERE comment_id = %s",
        (comment_id,)
    )
    db.commit()
    curr.close()

    return redirect(request.referrer)


#route for role update form
@app.route('/role_update', methods=['POST', 'GET'])
@login_required
def role_update():

    form = RoleUpdateForm()

    if form.validate_on_submit():
        #add the user id and role from form to role_update table with a new db method

        add_request(current_user.id, form.role.data)

        return render_template('role_update_form.html', form=form, submit_complete=True)
    

    return render_template('role_update_form.html', form=form, submit_complete=False)


#route for role update form
@app.route('/view_update_requests', methods=['POST', 'GET'])
@login_required
def view_update_requests():

    requests = get_requests()

    return render_template('update_requests.html', requests = requests)


#route for approving role update request
@app.route('/approve_role_update/<new_role>/<username>/<int:request_id>')
@login_required
def approve_role_update(new_role, username, request_id):

    #check if mod or admin has already made decision
    decision_complete = check_decision(request_id)

    #if decision already made, do not allow current user to make new one
    if decision_complete == True:
        flash("Decision already made! Please refresh.") 
        return redirect("/view_update_requests")
    
    #if decision not made, approve the request and redirect to view_update_requests
    approve_new_role(new_role, username, request_id)

    return redirect(request.referrer)



#route for rejecting role update request
@app.route('/reject_role_update/<int:request_id>')
@login_required
def reject_role_update(request_id):

    #check if mod or admin has already made decision
    decision_complete = check_decision(request_id)

    #if decision already made, do not allow current user to make new one
    if decision_complete == True:
        flash("Decision already made! Please refresh.") 
        return redirect("/view_update_requests")
    
    #if decision not made, reject the request and redirect to view_update_requests
    reject_new_role(request_id)

    return redirect(request.referrer)

with app.app_context():
    init_db()

if __name__ == '__main__':
    print("Starting AnonReview upload server local host")
    app.run()
