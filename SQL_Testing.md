# SQL_TESTING.md
## Project Milestone 5: SQL DESIGN

**Project:** AnonReview <br>
**Purpose:** Database design and testing specifications for developers

---
## Overview
This document describes AnonReviews database schema, the relationship between tables, and the methods which 
will be used to access the data.

This document answers the following questions:
- What tables exist in the database?
- What are the fields, datatypes and constraints for each table?
- What is the relationship between the tables?
- What are the methods which will be used to access the data.
- What pages use data from the database and how is it accessed?
- How will we test the schema and access routines?

# Database Tables
Our current implementation uses the following tables:
- categories
- users
- posts
- comments
- comment_votes

Each of these tables is described below. <br><br> *Note: All tests are conditioned on the database running*

---

## 1) Table: categories

### Table Description
Stores information for the different categories of posts a user can choose.

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|category_id|Unique category identifier|Primary Key|
|name| Stores the category name|Not Null|
|description|Stores the category description| | 


### Relationships
- One-to-many with *posts*
  
### Table Tests
**Use Case:** Querying Categories <br>
**Description:** All available categories are queried and displayed when creating a post or using the dashboard <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Query Category names <br>

**Expected Result:** All categories are returned <br>
**Actual Result:** <br>
**Status:** <br>
**Post-conditions:** Categories persist

---

## 2) Table: users

### Table Description
Stores information for users of AnonReview.

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|user_id|Unique Category Identifier|Primary Key|
|username|Stores the users chosen username|Unique, Not Null|
|email|Stores Users email address|Unique, Not Null|
|password_hash|Stores users hashed password|Not Null|
|role|Stores the users role|Check role is valid, Default is "Student"|
|is_active|Bool to store if user is active|Check int is 0 or 1, Default is 1|
|created_at|Stores when user is created|Default is current timestamp|

### Relationships
* One-to-many with *posts*
* One-to-many with *comments*
* One-to-many with *comment_votes*
### Table Tests
**Use Case:** Registering a User <br>
**Description:** Verify a new user is stored in the database correctly when registered <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Insert Valid users row
2. Query user by user_id <br>

**Expected Result:** User is inserted in table and able to be queried succesfully by user_id <br>
**Actual Result:** <br>
**Status:** <br>
**Post-conditions:** User persists
---

## 3) Table: posts

### Table Description
Stores information about users posts to the AnonReview platform 

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|post_id|Unique Category Identifier|Primary Key|
|user_id|Foreign key related to users table|Foreign Key, Not Null|
|category_id|Foreign key related to categories table|Foreign Key|
|title|Title of post| Not Null|
|body|Body text of post| Not Null|
|attachment_name| Name of attached document (if exists)| |
|attachment_blob| Binary blob for attached document (if exists)| |
|attachment_type| file type of attached document| |
| anon_name| Anonymous name of user for display| |
|Created_at| Time when post was created| Default is current timestamp|
|Updated_at| Time when post was updated | Default is current timestamp|

### Relationships
* Many-to-one with *categories*
* Many-to-one with *users*
* One-to-many with *comments*
### Table Tests
**Use Case:** Creating a post <br>
**Description:** Verify a post is succesfully inserted when a post is created <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Insert Valid posts row
2. Query user by post_id <br>

**Expected Result:** Post is inserted in table and able to be queried succesfully by post_id <br>
**Actual Result:** <br>
**Status:** <br>
**Post-conditions:** Post persists
---

## 4) Table: comments

### Table Description
Stores any comments related to a particular post 

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|comment_id|Unique category identifier|Primary Key|
|post_id|Foreign key related to posts|Foreign Key, Not Null|
|user_id|Foreign key related to users|Foreign Key, Not Null|
|anon_name|Anonymous name for user| |
|body|Stores comment text| Not Null|
|comment_anchor| Anchor for comment (if needed) | |
|line number|Line number of document if comment is related to an uploaded document | |
|upvotes|Stores number of upvotes for comment| Default is zero|
|downvotes|Stores number of downvotes for comment| Default is zero|
|created_at|Stores when comment was created| Default is current timestamp|


### Relationships
* Many-to-one with *posts*
* Many-to-one with *users*
* One-to-many with *comment_votes*
### Table Tests
**Use Case:** Creating a comment <br>
**Description:** Verify a post is succesfully inserted when a comment is created <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Insert Valid comment row
2. Query user by comment_id <br>

**Expected Result:** Comment is inserted in table and able to be queried succesfully by comment_id <br>
**Actual Result:** <br>
**Status:** <br>
**Post-conditions:** Comment persists

---

## 5) Table: comment_votes

### Table Description

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|id|Unique Table identifier| Primary Key|
|user_id| Foreign key related to users table| Foreign Key|
|comment_id|Foreign Key related to comments table| Foreign Key|
|vote_type| Type of vote (up or down) for record| |

### Relationships
* Many-to-one with *users*
* Many-to-one with *comments*
### Table Tests
**Use Case:** Voting on a comment <br>
**Description:** Verify the comment vote is inserted correctly to the comment_votes table <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Insert Valid comment_votes row
2. Query user by id <br>

**Expected Result:** Comment_vote is inserted correctly <br>
**Actual Result:** <br>
**Status:** <br>
**Post-conditions:** Comment_vote persists

---

# Data Access Methods
Each table has at least one access method.

---

# Access Method: 

### Description

### Parameters

### Tests

---

# Access Method: 

### Description

### Parameters

### Tests

---

# Access Method: 

### Description

### Parameters

### Tests

---

# Access Method: 

### Description

### Parameters

### Tests

---

# Access Method: 

### Description

### Parameters

### Tests

---

# Access Method: 

### Description

### Parameters

### Tests

---

# Access Method: 

### Description

### Parameters

### Tests

---

# Access Method: 

### Description

### Parameters

### Tests

---

# Access Method: 

### Description

### Parameters

### Tests

---

# Access Method: 

### Description

### Parameters

### Tests

---

# Page Data Access Tests
