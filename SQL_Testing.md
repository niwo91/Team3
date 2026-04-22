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
- reports
- role_update

Each of these tables is described below. <br><br> *Note: All tests are conditioned on the database running*

---

## 1) Table: categories

### Table Description
Stores information for the different categories of posts a user can choose.

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|category_id|Unique table identifier for categories|Primary Key|
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
**Actual Result:** All categories were returned <br>
**Status:** Pass <br>
**Post-conditions:** Categories persist

---

## 2) Table: users

### Table Description
Stores information for users of AnonReview.

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|user_id|Unique Table Identifier for users|Primary Key|
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
* One-to-many with *reports*
* One-to-many with *role_update*
### Table Tests
**Use Case:** Registering a User <br>
**Description:** Verify a new user is stored in the database correctly when registered <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Insert Valid users row
2. Query user by user_id <br>

**Expected Result:** User is inserted in table and able to be queried succesfully by user_id <br>
**Actual Result:** User was inserted into table and was able to be queried succesfully <br>
**Status:** Pass <br>
**Post-conditions:** User persists

---

## 3) Table: posts

### Table Description
Stores information about users posts to the AnonReview platform 

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|post_id|Unique Table Identifier for posts|Primary Key|
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
|reported|Bool of if the post has gotten reported| Default is 0|

### Relationships
* Many-to-one with *categories*
* Many-to-one with *users*
* One-to-many with *comments*
* one-to-many with *reports*
### Table Tests
**Use Case:** Creating a post <br>
**Description:** Verify a post is succesfully inserted when a post is created <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Insert Valid posts row
2. Query user by post_id <br>

**Expected Result:** Post is inserted in table and able to be queried succesfully by post_id <br>
**Actual Result:** Post inserted succesfully <br>
**Status:** Pass <br>
**Post-conditions:** Post persists

---

## 4) Table: comments

### Table Description
Stores any comments related to a particular post 

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|comment_id|Unique Table identifier for comments|Primary Key|
|post_id|Foreign key related to posts|Foreign Key, Not Null|
|user_id|Foreign key related to users|Foreign Key, Not Null|
|anon_name|Anonymous name for user| |
|body|Stores comment text| Not Null|
|comment_anchor| Anchor for comment (if needed) | |
|line number|Line number of document if comment is related to an uploaded document | |
|upvotes|Stores number of upvotes for comment| Default is zero|
|downvotes|Stores number of downvotes for comment| Default is zero|
|created_at|Stores when comment was created| Default is current timestamp|
|reported|Bool of if the comment has gotten reported| Default is 0|


### Relationships
* Many-to-one with *posts*
* Many-to-one with *users*
* One-to-many with *comment_votes*
* One-to-many with *reports*
### Table Tests
**Use Case:** Creating a comment <br>
**Description:** Verify a post is succesfully inserted when a comment is created <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Insert Valid comment row
2. Query user by comment_id <br>

**Expected Result:** Comment is inserted in table and able to be queried succesfully by comment_id <br>
**Actual Result:** Comment inserted succesfully <br>
**Status:** Pass <br>
**Post-conditions:** Comment persists

---

## 5) Table: comment_votes

### Table Description
Stores data for upvotes and downvotes on comments

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|id|Unique Table identifier for comment_votes| Primary Key|
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
**Actual Result:** Comment vote inserted correctly <br>
**Status:** Pass <br>
**Post-conditions:** Comment_vote persists

---

## 6) Table: reports

### Table Description
Table to hold information for "reported" comments/Posts on the AnonReview platform.

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|Report_id|Unique table identifier for reports|Primary Key|
|user_id| Foreign Key which references the user table|Foreign Key, Not Null|
|post_id|Foreign Key which references the posts table|Foreign Key, Not Null|
|comment_id|Foreign Key which references the comments table|Foreign Key|
|reason| Reason for flag| |
|created_at| Time report was created| Defaults to current timestamp|


### Relationships
- Many-to-one relationship with *users*
- Many-to-one relationship with *posts*
- Many-to-one relationship with *comments*
  
### Table Tests
**Use Case:** Reporting a comment or post <br>
**Description:** Verify the report is inserted correctly to the reports table <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Insert Valid reports row <br>
2. Query report by report_id <br>

**Expected Result:** report is inserted correctly <br>
**Actual Result:** Report inserted correctly <br>
**Status:** Pass <br>
**Post-conditions:** report persists

---

## 7) Table: role_update

### Table Description
Stores requests for role updates (from student to teacher/moderator).

### Fields
| Field Name | Field Description | Field Constraints |
|------------|-------------------|-------------------|
|request_id|Unique Table Identifier for role updates|Primary Key|
|user_id|ID of user who made request|Foreign Key, Not Null|
|new_role|New role that user has selected|Value can either be 'teacher' or 'moderator'|
|decision_complete|Bool to check if mod/admin has taken decision on request|Default is 0 (incomplete decision)|
|created_at|Stores when request is created|Default is current timestamp|

### Relationships
* Many-to-one with *users*
### Table Tests
**Use Case:** Adding a request <br>
**Description:** Verify a new request has been added to the table <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Insert valid role_update row
2. Query request by request_id <br>

**Expected Result:** Request is inserted in table and able to be queried succesfully by request_id <br>
**Actual Result:** Request inserted succesfully <br>
**Status:** Pass<br>
**Post-conditions:** Request persists

**Use Case:** Update decision completion <br>
**Description:** Verify that decision_complete is set to 1 after mod/admin reject/accepts request <br>
**Pre-conditions:** Database running <br>

**Test Steps:**
1. Set decision_complete to 1 for any row/rows in role_update table
2. Query role_update by request_id <br>

**Expected Result:** decision_complete should be set to one for selected row/rows <br>
**Actual Result:** Decision set appropiately<br>
**Status:** Pass <br>
**Post-conditions:** decision_complete value should persist 


---

# Data Access Methods
Each table has at least one access method.

---

# Access Method: check_user

### Description
Compares login form data to users table data for login

### Parameters
- username (string)
- password (string)

### Return Values
- Tuple containing list of user data required for user object, bool for valid password (True if valid password), and active status from is_active column (True if user is not banned or suspended).

### Tests

**Use Case Name:** Verify valid login 

**Pre-conditions:** User should exist 

**Test Steps:**

1. Enter username and password for user in login form

**Expected Result:** [user_id, username, role], valid_password = True, is_active = True returned

**Post-conditions:** User should be logged in and redirected to dashboard

---

**Use Case Name:** Identify invalid login credentials (nonexistent username)

**Pre-conditions:** Username should not exist in users table

**Test Steps:**

1. Enter nonexistent username in login form

**Expected Result:** None, valid_password = False, is_active = False returned

**Post-conditions:** User should stay on login page and see message stating that credentials were invalid (message does not specify whether username, password, or both were incorrect)

---

**Use Case Name:** Identify invalid login credentials (incorrect password)

**Pre-conditions:** User should exist, hashed password in database should not match password entered in form when verified

**Test Steps:**
1. Enter incorrect password for user

**Expected Result:** [user_id, username, role], valid_password = False, is_active = True/False (depending on is_active column) returned

**Post-conditions:** User should stay on login page and see message stating that credentials were invalid (message does not specify whether username, password, or both were incorrect)

---

**Use Case Name:** Identify inactive user

**Pre-conditions:** User should exist, is_active column in users table = False

**Test Steps:**

1. Enter correct username and password for user in login form

**Expected Result:** [user_id, username, role], valid_password = True, is_active = False

**Post-conditions:** User should stay on login page and see message stating that they were banned or suspended, and should contact admin for more details

---

# Access Method: check_registration

### Description
Compares registration form data to users table data for registration

### Parameters
- username (string)
- email (string)

### Return Values
- Tuple containing Boolean values for whether username exists, whether email exists

### Tests

**Use Case Name:** Verify valid registration data

**Pre-conditions:** Users with entered username and/or email should not exist

**Test Steps:**

1. Enter a unique username and email in the registration form, along with password (minimum 10 characters) and selected user role

**Expected Result:** existing_username = False, existing_email = False returned

**Post-conditions:** register_user should be called

---

**Use Case Name:** Identify existing username

**Pre-conditions:** User with entered username should exist

**Test Steps:**

1. Enter an existing username in the registration form, along with email, password (minimum 10 characters) and selected user role

**Expected Result:** existing_username = True, existing_email = True/False (depends on whether entered email exists) returned

**Post-conditions:** register_user should not be called, user should stay on registration page and see message stating that account with entered username exists

---

**Use Case Name:** Identify existing email

**Pre-conditions:** User with entered email should exist

**Test Steps:**

1. Enter a unique username and existing email in the registration form

**Expected Result:** existing_username = False, existing_email = True returned

**Post-conditions:** register_user should not be called, user should stay on registration page and see message stating that account with entered email exist


---

# Access Method: register_user

### Description
Adds a new record to users table on successful registration. Only called if check_registration returns (False, False) and password re-entry is correct in registration form.

### Parameters
- username (string)
- email (string)
- password (string)
- role (string)

### Return Values

None

### Tests

**Use Case Name:** Register user

**Pre-conditions:** User with entered username and password should not exist

**Test Steps:**

1. Enter a unique username and email in the registration form, along with password (minimum 10 characters) and selected user role

**Expected Result:** User record added to users table

**Post-conditions:** User should be redirected to login page and notified that registration was successful. User should be able to log in successfully.


---

# Access Method: get_categories

### Description
Returns all categories in the category table

### Parameters
None

### Tests
**Use Case Name:** Fetch categories to display when creating a post or viewing the dashboard

**Pre-conditions:** Database is running, At least one category exists

**Test Steps:**

1. Query the database to ensure it returns all category names

**Expected Result:** All Category names are returned

**Post-conditions:** Category records persist.

---

# Access Method: create_post

### Description
Adds a post record to the database

### Parameters
user_id, category_id, title, body, attachment_name, attachment_blob, attachment_type

### Tests
**Use Case Name:** Confirm the record has been inserted into the posts table

**Pre-conditions:** Database is running

**Test Steps:**

1. Query the database to ensure it returns the record correctly and correctly creates an incremented post_id.

**Expected Result:** Record is inserted correctly, post_id is incremented correctly

**Post-conditions:** Category records persist.

---

# Access Method: get_post

### Description
Fetches data for a post from the *posts* database

### Parameters
Post ID

### Tests
**Use Case Name:** Query the post by id for display in view_post

**Pre-conditions:** Database is running

**Test Steps:**

1. Query the database and ensure all data is pulled correctly for a post with the post_id given

**Expected Result:** All data is retrieved correctly.

**Post-conditions:** Post record persists.

---

# Access Method: delete_a_post

### Description
Deletes a post

### Parameters
post_id

### Tests
**Use Case Name:** Deletes the post when clicking on delete post

**Pre-conditions:** Database is running

**Test Steps:**

1. Delete the record from the posts table and all associated comment records.

**Expected Result:** All data is deleted correctly.

**Post-conditions:** post record does not persist.

---

# Access Method: add_a_comment

### Description
Adds a comment to a post

### Parameters
post_id, user_id, body, anon_name, line_number

### Tests
**Use Case Name:** Confirm the record has been inserted into the comments table

**Pre-conditions:** Database is running

**Test Steps:**

1. Query the database to ensure it returns the record correctly and correctly creates an incremented comment_id.

**Expected Result:** Record is inserted correctly, comment_id is incremented correctly

**Post-conditions:** Comment records persist.

---

# Access Method: get_comment

### Description
Fetches a comment from the database for display on the post related to the comment.

### Parameters
post_id, user_id

### Tests
**Use Case Name:** Query comments for all comments related to a particular post, display comment body and anonymous user name.

**Pre-conditions:** Database is running

**Test Steps:**

1. Query the database and ensure all data is pulled correctly for comments related to a particular post

**Expected Result:** All data is retrieved correctly.

**Post-conditions:** Comment record persists.

---

# Access Method: get_votes

### Description
Fetch downvotes and upvotes related to a particular comment

### Parameters
comment_id

### Tests
**Use Case Name:** Query comment_votes for all votes related to a particular comment

**Pre-conditions:** Database is running

**Test Steps:**

1. Query the database and ensure all data is pulled correctly for comments_votes related to a particular comment.

**Expected Result:** All data is retrieved correctly.

**Post-conditions:** Comment_vote record persists.

---

# Access Method: vote_a_comment

### Description
Vote up or down on a particular comment

### Parameters
user_id, comment_id, vote_type

### Tests
**Use Case Name:** Vote up or down on a particular comment

**Pre-conditions:** Database is running

**Test Steps:**

1.  Query the database to ensure it returns the record correctly and correctly creates an incremented id (primary key)for the table.

**Expected Result:** All data is retrieved correctly.

**Post-conditions:** Comment_vote record persists.

---

# Access Method: Flag_item

### Description
Adds a record for a comment and/or a post which has been flagged for review

### Parameters
post_id, comment_id

### Tests
**Use Case Name:** Confirm the record has been inserted into the records table

**Pre-conditions:** Database is running

**Test Steps:**

1. Query the database to ensure it returns the reported/flagged item has been added to the reports table.

**Expected Result:** Record is inserted correctly, report_id is incremented correctly

**Post-conditions:** reports records persist.

---

# Access Method: add_request

### Description
Inserts a request for a role update into the role_update table.

### Parameters
- user_id (int)
- new_role (string)

### Return Values
- None

### Tests

**Use Case Name:** Verify request has been added 

**Pre-conditions:** User should have role 'student'

**Test Steps:**

1. Navigate to Update Role section on dashboard
2. Select role from dropdown menu ('teacher' or 'moderator')
3. Submit form

**Expected Result:** Request should be added to role update as a row

**Post-conditions:** Request successfully submitted by user, persists in database

---

# Access Method: get_requests

### Description
Retrieve all incomplete requests (decision_complete == 0) from role_update table.

### Parameters
None

### Return Values
- List of rows (requests) where decision_complete == 0.

### Tests

**Use Case Name:** Verify that all rows where decision_complete == 0 are being returned 

**Pre-conditions:** User should have role 'moderator' or 'admin', undecided request(s) should have been submitted through Update Role form previously

**Test Steps:**

1. Log in as user with role 'moderator' or 'admin'
2. Navigate to Role Update Requests section

**Expected Result:** Method should retrieve all rows where decision_complete == 0

**Post-conditions:** User should be able to view all submitted (but incomplete) requests


---

# Access Method: check_decision

### Description
Checks whether the decision for a request is already complete (decision_complete == 1).

### Parameters
- request_id (int)

### Return Values
- Value of decision_complete for specific request_id (1 or 0)

### Tests

**Use Case Name:** Check that two users cannot update decision

**Pre-conditions:** User should have role 'moderator' or 'admin'. Two users with either role should exist. Two testers should be available for testing. Undecided request(s) should have been submitted through Update Role form previously

**Test Steps:**

1. Both developers log in on either of the two moderator/admin accounts
2. Both navigate to Role Update Requests section
3. First tester approves/rejects a request
4. Second tester should click approve/reject for same request

**Expected Result:** decision_complete successfully updated by first tester, decision persists through other decision attempts

**Post-conditions:** First tester should see approved/rejected request removed from list of requests. When second tester tries to take decision on same request, flash message should appear informing them that decision has already been made. Second tester's decision should not override first tester's.

---

# Access Method: approve_new_role

### Description
Approves a role update for the user that made request, changes their role accordingly. Sets decision_complete to 1.

### Parameters
- new_role (string)
- username (string)
- request_id (int)

### Return Values
- None

### Tests

**Use Case Name:** Verify role update on approval

**Pre-conditions:** User should be logged in with role 'moderator' or 'admin'. Undecided request(s) should have been submitted through Update Role form previously

**Test Steps:**

1. Log in as moderator/admin
2. Navigate to Role Update Requests section
3. Approve the submitted request
4. Log out, log in as user who submitted request

**Expected Result:** Role should successfully be updated in users table for user that submitted request. decision_complete should be set to 1 for the request.

**Post-conditions:** Admin/Moderators should not be able to see the request on reload of page. When user logs in, their permissions should successfully be updated to those of their new role (e.g. post deletion, no visible Update Role section for teachers, Role Requests section replaces Update Role section for moderators

---

# Access Method: reject_new_role

### Description
Rejects a role update for the user that made request, does not change their role. Sets decision_complete to 1.

### Parameters
- request_id (int)

### Return Values
- None

### Tests

**Use Case Name:** Verify role update rejection

**Pre-conditions:** User should be logged in with role 'moderator' or 'admin'. Undecided request(s) should have been submitted through Update Role form previously

**Test Steps:**

1. Log in as moderator/admin
2. Navigate to Role Update Requests section
3. Reject the submitted request
4. Log out, log in as user who submitted request

**Expected Result:** Role should not be updated in users table for user that submitted request. decision_complete should be set to 1 for the request.

**Post-conditions:** Admin/Moderators should not be able to see the request on reload of page. When user logs in, their permissions should still be student permissions.

---


## Page-to-Database Mapping

| Page | Tables Accessed |
|----|----------------|
| Login | users |
|Registration| Users
| Dashboard | users, categories, posts |
| view post | posts, comments, comment_votes |
| create post| users, posts, categories|
| index page| None|
| Update Role page| role_update|
| Role Update Requests page| role_update, users|

---
# Page Data Access Tests

**Use Case Name:** Dashboard shows categories and posts

**Description:** Dashboard should show all recent posts and you should be able to query by categories

**Pre-conditions:** User is logged into dashboard, posts exist, categories exists

**Test Steps:** 
1. Login to the dashboard
   
**Expected Result:** Dashboard displays category filters and all recent posts

**Post-conditions:** None

---

**Use Case Name:** View post

**Description:** Viewing a post should show all post related content along with any comments and comment votes.

**Pre-conditions:** User is logged in and viewing a post

**Test Steps:** 
1. Login to the dashboard
2. View a post
   
**Expected Result:** Post displays data and comments correctly.

**Post-conditions:** None

---

**Use Case Name:** View Update Role form

**Description:** User logged in as 'student' should be able to navigate to and view the Update Role form

**Pre-conditions:** User is logged in with role 'student' and is on dashboard

**Test Steps:** 
1. Log in as user with role 'student'
2. Navigate to Update Role section
   
**Expected Result:** User should be able to:
- View Update Role form
- Interact with dropdown menu
- Click submit button
- View success message on submit

**Post-conditions:** List of role update requests should be updated on moderator/admin accounts when viewing Role Update Requests page

---

**Use Case Name:** View Role Update Requests page

**Description:** User logged in as 'moderator' or 'admin' should be able to navigate to and view the Role Update Requests page

**Pre-conditions:** User is logged in with role 'moderator' or 'admin' and is on dashboard

**Test Steps:** 
1. Log in as user with role 'moderator' or 'admin'
2. Navigate to Role Update Requests section
   
**Expected Result:** User should be able to:
- View Role Update Requests page
- View list of requests
- Be able to interact with 'Approve' and 'Reject' buttons
- Request should be removed from page on 'Approve' or 'Reject' button click

**Post-conditions:** List of role update requests should be updated on moderator/admin accounts when viewing Role Update Requests page

---

## Notes
- Constraints enforced at DB
- Tests executable via integration test suite

