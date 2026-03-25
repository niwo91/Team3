import unittest
import testDB_setup
import methods
from flask import g
from basic_app import app
from passlib.hash import pbkdf2_sha512
import os

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


'''
Purpose: Class for database access unit tests (table: categories)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbCategory_Test
'''

#class dbCategory_Test:



'''
Purpose: Class for database access unit tests (table: posts)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbPosts_Test
'''

#class dbPosts_Test:



'''
Purpose: Class for database access unit tests (table: comments)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbComments_Test
'''

#class dbComments_Test:


'''
Purpose: Class for database access unit tests (table: comment_votes)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbCommentVotes_Test
'''

#class dbCommentVotes_Test:


'''
Purpose: Class for database access unit tests (table: reports)
Parameters: None
Usage: In terminal run: python3 test_dbMethods.py dbReports_Test
'''

#class dbReports_Test:




if __name__ == '__main__':

    #required for db connection and querying
    with app.app_context():
        unittest.main()
