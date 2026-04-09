# methods.py
# Database Access Methods for AnonReview

from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha512
from flask import g
import sqlite3
from Constants import *

# DB Helpers 

def get_db():
    '''
    Connects to db, or returns active db if already connected
    '''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

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


def register_user(username, email, password):
    db = get_db()
    hashed_password = pbkdf2_sha512.hash(password)

    db.execute(
        """
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (username, email, hashed_password)
    )
    db.commit()

# 4. get_categories


def get_categories():
    return query_db("SELECT * FROM categories")

# 5. create_post

def create_a_post(user_id, category_id, title, body,
                attachment_name=None, attachment_blob=None, attachment_type=None):

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO posts (user_id, category_id, title, body,
                           attachment_name, attachment_blob, attachment_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, category_id, title, body,
         attachment_name, attachment_blob, attachment_type)
    )

    db.commit()
    
    return cursor

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
        """
        SELECT comment_id, body, anon_name, line_number, upvotes, downvotes
        FROM comments
        WHERE post_id = ?
        ORDER BY created_at ASC
        """,
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
    
    if post_id:
        db.execute("UPDATE posts SET reported = 1 WHERE post_id = ?", (post_id,))

    db.commit()




#13. add request

#adds a user request for a role update to the role_update table
def add_request(user_id, new_role):
    db = get_db()

    db.execute(
        """
        INSERT INTO role_update (user_id, new_role)
        VALUES (?, ?)
        """,
        (user_id, new_role)
    )
    db.commit()



#14. get_requests

#gets all role update requests from the role_update table (where decision is incomplete)
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




#15. check_decision

#checks if decision for user role update has already been completed. returns True if complete, False otherwise
def check_decision(request_id):

    db = get_db()

    decision_complete = query_db(
        """
        SELECT decision_complete FROM role_update
        WHERE request_id = ?
        """,
        (request_id, )
    )

    return decision_complete




#16. approve_new_role

#method to approve user role update
def approve_new_role(new_role, username, request_id):
    db = get_db()

    #set new role for user
    db.execute(
        """
        UPDATE users SET role = ? WHERE username = ?
        """,
        (new_role, username)
    )

    #mark decision as complete
    db.execute(
        """
        UPDATE role_update SET decision_complete = ? WHERE request_id = ?
        """,
        (1, request_id)
    )
    db.commit()

    


#17. reject_new_role

#method to reject user role update
def reject_new_role(request_id):
    db = get_db()

    #mark decision as complete
    db.execute(
        """
        UPDATE role_update SET decision_complete = ? WHERE request_id = ?
        """,
        (1, request_id)
    )
    db.commit()
    


