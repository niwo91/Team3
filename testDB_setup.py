import sqlite3

'''
Purpose: Creates a database with given filename, creates tables according to schema
Parameters: db_filename (name of database being created)
Usage: create(<filename with extension .db as string>)
'''
def create(db_filename):
    conn = sqlite3.connect(db_filename)
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    with open("schema.sql") as schema:
        c.executescript(schema.read())

    conn.commit()
    conn.close()

'''
Purpose: Add rows to each table (copied from anonreview.db)
Parameters: db_filename (name of database you are adding to)
Usage: fill(<filename with extension .db as string>)
'''
def fill(db_filename):
    conn = sqlite3.connect(db_filename)
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
    c.execute("ATTACH DATABASE 'anonreview.db' AS 'anonreview';")
    c.execute("INSERT INTO users SELECT * FROM anonreview.users;")
    c.execute("INSERT INTO categories SELECT * FROM anonreview.categories;")

    conn.commit()
    conn.close()