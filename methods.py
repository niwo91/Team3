# methods.py
# Database Access Methods for AnonReview

from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha512
from flask import g
import sqlite3

# DB Helpers 

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('test.db')
        g.db.row_factory = sqlite3.Row
    return g.db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv



# 1. check_user


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


# 2. check_registration


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

# 3. register_user


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

# 4. get_categories


def get_categories():
    return query_db("SELECT * FROM categories")

# 5. create_post

def create_a_post(user_id, category_id, title, body,
                attachment_name=None, attachment_blob=None, attachment_type=None):

    db = get_db()

    db.execute(
        """
        INSERT INTO posts (user_id, category_id, title, body,
                           attachment_name, attachment_blob, attachment_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, category_id, title, body,
         attachment_name, attachment_blob, attachment_type)
    )

    db.commit()

# 6. get_post


def get_post(post_id):
    return query_db(
        "SELECT * FROM posts WHERE post_id = ?",
        (post_id,),
        one=True
    )

# 7. delete_post

def delete_post(post_id):
    db = get_db()

    db.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
    db.execute("DELETE FROM posts WHERE post_id = ?", (post_id,))

    db.commit()


# 8. add_comment


def add_a_comment(post_id, user_id, body, anon_name, line_number=None):
    db = get_db()

    db.execute(
        """
        INSERT INTO comments (post_id, user_id, body, anon_name, line_number)
        VALUES (?, ?, ?, ?, ?)
        """,
        (post_id, user_id, body, anon_name, line_number)
    )

    db.commit()

# 9. get_comments


def get_comments(post_id):
    return query_db(
        "SELECT * FROM comments WHERE post_id = ? ORDER BY created_at DESC",
        (post_id,)
    )


# 10. get_votes


def get_votes(comment_id):
    return query_db(
        "SELECT * FROM comment_votes WHERE comment_id = ?",
        (comment_id,)
    )

# 11. vote_comment


def vote_a_comment(user_id, comment_id, vote_type):
    db = get_db()

    existing = query_db(
        "SELECT * FROM comment_votes WHERE user_id = ? AND comment_id = ?",
        (user_id, comment_id),
        one=True
    )

    if existing:
        return False

    db.execute(
        """
        INSERT INTO comment_votes (user_id, comment_id, vote_type)
        VALUES (?, ?, ?)
        """,
        (user_id, comment_id, vote_type)
    )

    if vote_type == "up":
        db.execute(
            "UPDATE comments SET upvotes = upvotes + 1 WHERE comment_id = ?",
            (comment_id,)
        )
    else:
        db.execute(
            "UPDATE comments SET downvotes = downvotes + 1 WHERE comment_id = ?",
            (comment_id,)
        )

    db.commit()
    return True


# 12. flag_item


def flag_item(user_id, post_id, comment_id=None, reason=None):
    db = get_db()

    db.execute(
        """
        INSERT INTO reports (user_id, post_id, comment_id, reason)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, post_id, comment_id, reason)
    )

    # Every comment is related to a post ID, this should allow us to report posts and comments
    if comment_id:
        db.execute("UPDATE comments SET reported = 1 WHERE comment_id = ?", (comment_id,))
    else:
        db.execute("UPDATE posts SET reported = 1 WHERE post_id = ?", (post_id,))

    db.commit()
