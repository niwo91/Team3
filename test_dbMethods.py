import unittest
import testDB_setup
import methods
from flask import g
from basic_app import app
from passlib.hash import pbkdf2_sha512
import os
import sqlite3

'''
Purpose: Class for database access unit tests (table: users)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbUsers_Test
'''
class dbUsers_Test(unittest.TestCase):

    #sets up temporary database for testing
    def setUp(self):

        testDB_setup.create("test.db")
        testDB_setup.fill("test.db")


    #closes db connection and removes temporary database if it exists
    def tearDown(self):

        db = g.pop('db', None)

        if db is not None:
            db.close()

        try:
            os.remove("test.db")
        except OSError:
            pass

    
    ###Tests for check_user

    
    #tests login for registered and active user
    def test_valid_user(self):
        
        user_data = methods.check_user('test_student', 'TestPass01')

        self.assertEqual(user_data, ([1, 'test_student', 'student'], True, True))


    #tests login for unregistered user
    def test_unreg_username(self):
        
        user_data = methods.check_user('test_new', 'TestPass01')

        self.assertEqual(user_data, (None, False, False))


    #tests login for registered and active user, incorrect password
    def test_incorrect_password(self):
        
        user_data = methods.check_user('test_student', 'TestPass011')

        self.assertEqual(user_data, ([1, 'test_student', 'student'], False, True))


    #tests login for registered but inactive user
    def test_inactive_user(self):

        #create an inactive user before testing db access
        hashed_pswd = pbkdf2_sha512.hash('TestPass03')

        methods.query_db('INSERT INTO users (username, email, password_hash, role, is_active) ' \
    'VALUES (?, ?, ?, ?, ?)', ['inactive_student', 'inactive_student@student.com', hashed_pswd, 'student', 0])
        
        user_data = methods.check_user('inactive_student', 'TestPass03')

        self.assertEqual(user_data, ([6, 'inactive_student', 'student'], True, False))


     ###Tests for check_registration

    
    def test_valid_registration(self):

        valid_reg_data = methods.check_registration('test_new', 'testnew@student.com')

        self.assertEqual(valid_reg_data, (False, False))


    def test_existing_username(self):

        existing_username_user = methods.check_registration('test_student', 'testnew@student.com')

        self.assertEqual(existing_username_user, (True, False))

    
    def test_existing_email(self):

        existing_email_user = methods.check_registration('test_new', 'test1@student.com')

        self.assertEqual(existing_email_user, (False, True))


     ###Tests for register_user


    def test_add_user(self):

        #make sure user does not exist first
        user_not_added = methods.check_user('test_new', 'TestNew01')

        self.assertEqual(user_not_added, (None, False, False))
        

        methods.register_user('test_new', 'testnew@student.com', 'TestNew01', 'student')

        user_added = methods.check_user('test_new', 'TestNew01')

        self.assertEqual(user_added, ([6, 'test_new', 'student'], True, True))



'''
Purpose: Class for database access unit tests (table: categories)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbCategory_Test
'''

class dbCategory_Test(unittest.TestCase):

    #sets up temporary database for testing
    def setUp(self):

        testDB_setup.create("test.db")
        testDB_setup.fill("test.db")

    #closes db connection and removes temporary database if it exists
    def tearDown(self):

        db = g.pop('db', None)

        if db is not None:
            db.close()

        try:
            os.remove("test.db")
        except OSError:
            pass

    def test_categories(self):

        categories = ("Homework", "Project", "Exam Prep", "General", "Code Review", "Reported Items")

        cats = methods.query_db("SELECT name FROM categories;")

        for i in range(len(cats)):
            self.assertEqual(cats[i][0], categories[i], "Issue with categories table")


'''
Purpose: Class for database access unit tests (table: posts)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbPosts_Test
'''

class dbPosts_Test(unittest.TestCase):

    #sets up temporary database for testing
    def setUp(self):

        testDB_setup.create("test.db")
        testDB_setup.fill("test.db")

    #closes db connection and removes temporary database if it exists
    def tearDown(self):

        db = g.pop('db', None)

        if db is not None:
            db.close()

        try:
            os.remove("test.db")
        except OSError:
            pass

    def test_create_post(self):

        # Test Normal create post 
        methods.create_post(1, 1, "Test_Title", "Test_Body")
        
        test_post = methods.query_db("SELECT * FROM posts")


        # post_id, user_id, category_id, title, body
        values = [1, 1, 1, "Test_Title", "Test_Body"]
       
        # Index by position in test post
        for i in range(5):
            self.assertEqual(test_post[0][i], values[i], "Issue with create_post method")

        # Test NULL value insertions
        with self.assertRaises(sqlite3.IntegrityError):
            methods.create_post(1, 1, None, "Test_Body")

        with self.assertRaises(sqlite3.IntegrityError):
            methods.create_post(1, 1, "Test_Post", None)

    def test_get_post(self):
        # Insert post
        methods.create_post(1, 1, "Test_Title", "Test_Body")

        # Get values for testing
        post = methods.query_db("SELECT * FROM posts WHERE post_id = ?;", (1,), one=True)
        post_method = methods.get_post(1)

        # Test
        self.assertEqual(post, post_method, "Issue with get_post method")

        
    def test_delete_post(self):
        # Insert post
        methods.create_post(1, 1, "Test_Title", "Test_Body")
        methods.add_comment(1, 2, "Test_comment", "Name")

        # Delete post
        methods.delete_post(1)

        # Test
        self.assertEqual(methods.get_post(1), None, "Issue with delete_post method")
        # Comments should return empty list
        self.assertEqual(methods.get_comments(1), [], "Issue with delete_post method")


'''
Purpose: Class for database access unit tests (table: comments)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbComments_Test
'''

class dbComments_Test(unittest.TestCase):

    #sets up temporary database for testing
    def setUp(self):

        testDB_setup.create("test.db")
        testDB_setup.fill("test.db")
        # Create test post
        methods.create_post(1, 1, "Test_Title", "Test_Body")


    #closes db connection and removes temporary database if it exists
    def tearDown(self):

        db = g.pop('db', None)

        if db is not None:
            db.close()

        try:
            os.remove("test.db")
        except OSError:
            pass

    def test_add_comment(self):

        methods.add_comment(1, 1, "Test_Body", "Test_Name")

        comments = methods.query_db("SELECT * FROM comments where post_id = ?;", (1,))

        # Should be one comment only
        self.assertEqual(len(comments), 1, "Issue with add_comment method")

        # Comment saved as a tuple, look at first five values
        comment = (1, 1, 1, "Test_Name", "Test_Body")

        self.assertEqual(comment, comments[0][:5], "Issue with add_comment method")

        # Test NULL value insertions
        with self.assertRaises(sqlite3.IntegrityError):
            methods.add_comment(None, 1, "Test_Body", "Test_Name")
        with self.assertRaises(sqlite3.IntegrityError):
            methods.add_comment(1, None, "Test_Body", "Test_Name")
        with self.assertRaises(sqlite3.IntegrityError):
            methods.add_comment(1, 1, None, "Test_Name")

    def test_get_comments(self):

        # Add Comments
        methods.add_comment(1, 1, "Test1B", "Test1N")
        methods.add_comment(1, 2, "Test2B", "Test2N")

        db_comments = methods.get_comments(1)

        # Should be two comments only
        self.assertEqual(2, len(db_comments), "Issue with get_comments method")
    
        # Look at first 5 in return row
        test_comments = [(1, 1, 1, "Test1N", "Test1B"), (2, 1, 2, "Test2N", "Test2B")]
        comments = [(db_comments[0][:5]), (db_comments[1][:5])]
        self.assertEqual(comments, test_comments, "Issue with get_comments method")


'''
Purpose: Class for database access unit tests (table: comment_votes)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbCommentVotes_Test
'''

class dbCommentVotes_Test(unittest.TestCase):

    #sets up temporary database for testing
    def setUp(self):

        testDB_setup.create("test.db")
        testDB_setup.fill("test.db")
        # Create test post and comment
        methods.create_post(1, 1, "Test_Title", "Test_Body")
        methods.add_comment(1, 1, "Test1B", "Test1N")

    #closes db connection and removes temporary database if it exists
    def tearDown(self):

        db = g.pop('db', None)

        if db is not None:
            db.close()

        try:
            os.remove("test.db")
        except OSError:
            pass

    def test_vote_comment(self):
        # Add comment votes, users must be different
        methods.vote_comment(2, 1, "up") 
        methods.vote_comment(1, 1, "down")

        upvotes = methods.query_db("SELECT upvotes FROM comments WHERE comment_id = ?;", (1,), one=True)
        downvotes = methods.query_db("SELECT downvotes FROM comments WHERE comment_id = ?;", (1,), one=True)

        # Both should be 1
        self.assertEqual(upvotes[0], 1, "Issue with vote_comments method")
        self.assertEqual(downvotes[0], 1, "Issue with vote_comments method")

        # Both should be in DB
        vote1 = methods.query_db("SELECT * FROM comment_votes WHERE id = ?", (1,), one=True)
        vote2 = methods.query_db("SELECT * FROM comment_votes WHERE id = ?", (2,), one=True)

        test1 = [1, 2, 1, "up"]
        test2 = [2, 1, 1, "down"]

        for i in range(4):
            self.assertEqual(vote1[i], test1[i], "Issue with vote_comments method")
            self.assertEqual(vote2[i], test2[i], "Issue with vote_comments method")
    
    def test_get_votes(self):
        # Add comment votes, users must be different
        methods.vote_comment(2, 1, "up")
        methods.vote_comment(1, 1, "down")

        test1 = [1, 2, 1, "up"]
        test2 = [2, 1, 1, "down"]

        comments = methods.get_votes(1)

        # length should be 2
        self.assertEqual(len(comments), 2, "Issue with get_votes method")

        for i in range(4):
            self.assertEqual(comments[0][i], test1[i], "Issue with get_votes method")
            self.assertEqual(comments[1][i], test2[i], "Issue with get_votes method")

'''
Purpose: Class for database access unit tests (table: reports)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbReports_Test
'''

class dbReports_Test(unittest.TestCase):

    #sets up temporary database for testing
    def setUp(self):

        testDB_setup.create("test.db")
        testDB_setup.fill("test.db")
        # Create test post and comment
        methods.create_post(1, 1, "Test_Title", "Test_Body")
        methods.add_comment(1, 1, "Test1B", "Test1N")

    #closes db connection and removes temporary database if it exists
    def tearDown(self):

        db = g.pop('db', None)

        if db is not None:
            db.close()

        try:
            os.remove("test.db")
        except OSError:
            pass

    def test_flag_item(self):

        # Test Null Value insert
        with self.assertRaises(sqlite3.IntegrityError):
            methods.flag_item(None, 1, 1, "Test_Reason")
        with self.assertRaises(sqlite3.IntegrityError):
            methods.flag_item(1, None, 1, "Test_Reason")

        # Flag post and comment
        methods.flag_item(1, 1, None, "Test_Reason_post")
        methods.flag_item(1, 1, 1, "Test_reason_comment")

        reports = methods.query_db("SELECT * FROM reports")
        
        report1 = [1, 1, 1, None, "Test_Reason_post"]
        report2 = [2, 1, 1, 1, "Test_reason_comment"]

        # Length should be 2
        self.assertEqual(len(reports), 2, "Issue with flag_item method")

        for i in range(5):
            self.assertEqual(reports[0][i], report1[i])
            self.assertEqual(reports[1][i], report2[i])

        # Test reported flag shows for comment and post
        reported1 = methods.query_db("SELECT reported FROM posts WHERE post_id = ?;", (1,), one=True)
        reported2 = methods.query_db("SELECT reported FROM comments WHERE comment_id = ?;", (1,), one=True)

        self.assertEqual(reported1[0], 1, "Issue with flag_item method")
        self.assertEqual(reported2[0], 1, "Issue with flag_item method")




if __name__ == '__main__':

    #required for db connection and querying
    with app.app_context():
        unittest.main()
