-- Reset tables (order matters because of foreign keys)
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT UNIQUE NOT NULL,
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role          TEXT CHECK(role IN ('student', 'teacher', 'admin', 'moderator'))
                  DEFAULT 'student',
    is_active     INTEGER CHECK(is_active IN (0, 1)) DEFAULT 1, --1 is active
    created_at    TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT
);

-- Posts table
CREATE TABLE posts (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    attachment_name TEXT,
    attachment_blob BLOB,
    attachment_type TEXT,
    anon_name TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    reported INTEGER CHECK(reported IN (0, 1)) DEFAULT 0, --0 is not reported
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Comments table
CREATE TABLE comments (
    comment_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id        INTEGER NOT NULL,
    user_id        INTEGER NOT NULL,
    anon_name      TEXT,
    body           TEXT NOT NULL,
    comment_anchor TEXT,
    line_number    INTEGER,
    upvotes        INTEGER DEFAULT 0,
    downvotes      INTEGER DEFAULT 0,
    created_at     TEXT DEFAULT CURRENT_TIMESTAMP,
    reported       INTEGER CHECK(reported IN (0, 1)) DEFAULT 0, --0 is not reported
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE comment_votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    comment_id INTEGER,
    vote_type TEXT,
    UNIQUE(user_id, comment_id),
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    comment_id INTEGER NOT NULL,
    reason TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id)
);
