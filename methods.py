# methods.py
# Database Access Methods for AnonReview

from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha512
from flask import g
import psycopg2
import psycopg2.extras
import os
from Constants import *

# DB Helpers 
def seed_users(cur):
    users = [
        ("test_student", "test1@student.com", "TestPass01", "student"),
        ("test_student2", "test2@student.com", "TestPass02", "student"),
        ("test_teacher", "teacher1@teacher.com", "TestTeach01", "teacher"),
        ("test_admin", "admin1@admin.com", "TestAdmin01", "admin"),
        ("test_mod", "mod1@mod.com", "TestModerator01", "moderator"),
    ]

    for username, email, password, role in users:
        hashed = pbkdf2_sha512.hash(password)

        cur.execute("""
        INSERT INTO users (username, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO NOTHING;
        """, (username, email, hashed, role))

def init_db():
    db = get_db()
    cur = db.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT CHECK(role IN ('student','teacher','admin','moderator')) DEFAULT 'student',
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Categories table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    );
    """)

    # Posts table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        post_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        category_id INTEGER,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        attachment_name TEXT,
        attachment_blob BYTEA,
        attachment_type TEXT,
        anon_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reported BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );
    """)

    # Comments table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        comment_id SERIAL PRIMARY KEY,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        anon_name TEXT,
        body TEXT NOT NULL,
        comment_anchor TEXT,
        line_number INTEGER,
        upvotes INTEGER DEFAULT 0,
        downvotes INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reported BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (post_id) REFERENCES posts(post_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    # Comment votes table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS comment_votes (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        comment_id INTEGER,
        vote_type TEXT,
        UNIQUE(user_id, comment_id),
        FOREIGN KEY (comment_id) REFERENCES comments(comment_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    # Reports table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        report_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        post_id INTEGER NOT NULL,
        comment_id INTEGER,
        reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (post_id) REFERENCES posts(post_id),
        FOREIGN KEY (comment_id) REFERENCES comments(comment_id)
    );
    """)

    # Role update table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS role_update (
        request_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        new_role TEXT CHECK(new_role IN ('teacher','moderator')),
        decision_complete BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    # Seed categories (including required one), but only if table is empty to avoid duplicates on multiple runs
    cur.execute("SELECT 1 FROM categories LIMIT 1")
    existing = cur.fetchone()
    if not existing:
        cur.execute("""
        INSERT INTO categories (name) VALUES
        ('Homework'),
        ('Project'),
        ('Exam Prep'),
        ('General'),
        ('Code Review'),
        ('Reported Items');
        """)
    seed_users(cur)
    db.commit()
    cur.close()
def get_db():
    if 'db' not in g:
        DATABASE_URL = os.environ.get("DATABASE_URL")
        g.db = psycopg2.connect(DATABASE_URL)
        g.db.cursor_factory = psycopg2.extras.DictCursor
    return g.db

def query_db(query, args=(), one=False):
    '''
    Used to query DB
    @param query The sqlite3 query for the database
    @param args A list of arguments to be used in query - replaces %s in query
    @param one Bool for returning one value or not
    @return list with query result
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# 1. check_user


def check_user(username, password):
    user = query_db(
        "SELECT * FROM users WHERE username = %s",
        (username,),
        one=True
    )

    if not user:
        return None, False, False

    valid_password = pbkdf2_sha512.verify(password, user["password_hash"])
    is_active = user["is_active"]

    return user, valid_password, is_active


# 2. check_registration


def check_registration(username, email):
    existing_username = query_db(
        "SELECT 1 FROM users WHERE username = %s",
        (username,),
        one=True
    )

    existing_email = query_db(
        "SELECT 1 FROM users WHERE email = %s",
        (email,),
        one=True
    )

    return bool(existing_username), bool(existing_email)

# 3. register_user


def register_user(username, email, password):
    db = get_db()
    hashed_password = pbkdf2_sha512.hash(password)
    curr = db.cursor()

    curr.execute(
        """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        """,
        (username, email, hashed_password)
    )
    curr.close()
    db.commit()

# 4. get_categories


def get_categories():
    return query_db("SELECT * FROM categories")

# 5. create_post

def create_a_post(user_id, category_id, title, body,
                attachment_name=None, attachment_blob=None, attachment_type=None):

    db = get_db()
    curr = db.cursor()

    curr.execute(
        """
        INSERT INTO posts (user_id, category_id, title, body,
                           attachment_name, attachment_blob, attachment_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING post_id
        """,
        (user_id, category_id, title, body,
         attachment_name, attachment_blob, attachment_type)
    )
    post_id = curr.fetchone()[0]
    curr.close()
    db.commit()
    
    return post_id

# 6. get_post


def get_post(post_id):
    return query_db(
        "SELECT * FROM posts WHERE post_id = %s",
        (post_id,),
        one=True
    )

# 7. delete_post

def delete_post(post_id):
    db = get_db()
    curr = db.cursor()

    curr.execute("DELETE FROM comments WHERE post_id = %s", (post_id,))
    curr.execute("DELETE FROM posts WHERE post_id = %s", (post_id,))

    curr.close()
    db.commit()


# 8. add_comment


def add_a_comment(post_id, user_id, body, anon_name, line_number=None):
    db = get_db()

    curr = db.cursor()

    curr.execute(
        """
        INSERT INTO comments (post_id, user_id, body, anon_name, line_number)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (post_id, user_id, body, anon_name, line_number)
    )
    curr.close()
    db.commit()

# 9. get_comments


def get_comments(post_id):
    return query_db(
        """
        SELECT comment_id, body, anon_name, line_number, upvotes, downvotes
        FROM comments
        WHERE post_id = %s
        ORDER BY created_at ASC
        """,
        (post_id,)
    )

# 10. get_votes


def get_votes(comment_id):
    return query_db(
        "SELECT * FROM comment_votes WHERE comment_id = %s",
        (comment_id,)
    )

# 11. vote_comment


def vote_a_comment(user_id, comment_id, vote_type):
    db = get_db()

    existing = query_db(
        "SELECT * FROM comment_votes WHERE user_id = %s AND comment_id = %s",
        (user_id, comment_id),
        one=True
    )

    if existing:
        return False

    curr = db.cursor()
    curr.execute(
        """
        INSERT INTO comment_votes (user_id, comment_id, vote_type)
        VALUES (%s, %s, %s)
        """,
        (user_id, comment_id, vote_type)
    )

    if vote_type == "up":
        curr.execute(
            "UPDATE comments SET upvotes = upvotes + 1 WHERE comment_id = %s",
            (comment_id,)
        )
    else:
        curr.execute(
            "UPDATE comments SET downvotes = downvotes + 1 WHERE comment_id = %s",
            (comment_id,)
        )
    curr.close()
    db.commit()
    return True


# 12. flag_item


def flag_item(user_id, post_id, comment_id=None, reason=None):
    db = get_db()
    curr = db.cursor()

    try:
        # Get Reported Items category ID FIRST
        row = query_db(
            "SELECT category_id FROM categories WHERE name = %s",
            ("Reported Items",),
            one=True
        )
        reported_category_id = row["category_id"] if row else None

        # Insert report
        curr.execute(
            """
            INSERT INTO reports (user_id, post_id, comment_id, reason)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, post_id, comment_id, reason)
        )

        # Mark comment as reported
        if comment_id is not None:
            curr.execute(
                "UPDATE comments SET reported = TRUE WHERE comment_id = %s",
                (comment_id,)
            )

        # Move post to Reported Items + mark reported
        if post_id is not None and reported_category_id is not None:
            curr.execute("""
                UPDATE posts
                SET reported = TRUE,
                    category_id = %s
                WHERE post_id = %s
            """, (reported_category_id, post_id))

        db.commit()

    except Exception as e:
        print("REPORT ERROR:", e)
        db.rollback()
        raise e

    finally:
        curr.close()



def add_request(user_id, new_role):
    db = get_db()

    curr = db.cursor()

    curr.execute(
        """
        INSERT INTO role_update (user_id, new_role)
        VALUES (%s, %s)
        """,
        (user_id, new_role)
    )
    curr.close()
    db.commit()


def get_requests():
    db = get_db()

    requests = query_db(
        """
        SELECT u.username, u.email, r.new_role, r.request_id
        FROM users as u
        INNER JOIN role_update AS r
        ON u.user_id = r.user_id
        WHERE r.decision_complete = 0

        """
    )
    
    return requests


#checks if decision for user role update has already been completed. returns True if complete, False otherwise
def check_decision(request_id):

    db = get_db()

    decision_complete = query_db(
        """
        SELECT decision_complete FROM role_update
        WHERE request_id = %s
        """,
        (request_id, ),
        one=True
    )

    return decision_complete["decision_complete"] if decision_complete else False



#method to approve user role update
def approve_new_role(new_role, username, request_id):
    db = get_db()

    #set new role for user
    curr = db.cursor()
    curr.execute(
        """
        UPDATE users SET role = %s WHERE username = %s
        """,
        (new_role, username)
    )

    #mark decision as complete
    curr.execute(
        """
        UPDATE role_update SET decision_complete = %s WHERE request_id = %s
        """,
        (1, request_id)
    )
    curr.close()
    db.commit()


#method to reject user role update
def reject_new_role(request_id):
    db = get_db()

    #mark decision as complete
    curr = db.cursor()
    curr.execute(
        """
        UPDATE role_update SET decision_complete = %s WHERE request_id = %s
        """,
        (1, request_id)
    )
    curr.close()
    db.commit()
    


