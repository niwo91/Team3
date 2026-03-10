# Web Pages Design.md

This document defines the planned web pages for AnonReview, as well as rendering and testing requirements.

# 1) Login Page

## Title

Login

## Page Description

This page allows users who are not currently in a session to log into their AnonReview account. If the user does not have an account, they can access the registration page from this page.

## Page Route

**Login** → `/login`

**Mockup for Login**
```
+------------------------------------------------------+
| Welcome to AnonReview!                               |                 |                                                      |
|------------------------------------------------------|
| Login                                                |
|                                                      |
| Username: [       ]                                  |
| Password: [       ]                                  |
| [Submit]                                             |
|                                                      |
| Don't have an account? Register!                     |
+------------------------------------------------------+
```

## Route Parameters:

None

## Query Parameters:

URL query parameter `?redirect=/path` if user tries to access protected pages outside a session (user redirected to login page)

## Link Destinations for Page

**Submit success** → `/dashboard` (redirect)
**Register** → `/register`
**Submit failure** → `/login` (show Login page with error message)

## Data Required to Render Page

1. UI state: username, password, validation errors
2. API: To be added
3. Auth State Storage: To be added

## Tests for Verifying Rendering of the Page

1. **Template elements rendered**
   - Page title is displayed
   - Page header is displayed
   - Username and Password entry fields are visible, user can enter data
   - Submit button is visible and clickable
   - Link to Registration page is visible and clickable
   - Error messages are visible if user credentials are invalid (credentials do not meet validation parameters, no matching account exists)
     

2.   **Redirect Behaviour**
   - If user credentials are valid, redirect to Dashboard page
   - If user is in session, redirect to Dashboard page
   
   
# 2) Registration Page

## Title

Register

## Page Description

This page allows users to create an AnonReview account. It also allows users to navigate to the Login page.

## Page Route

**Register** → `/register`

**Mockup for Registration**
```
+------------------------------------------------------+
| Welcome to AnonReview!                               |                 |                                                      |
|------------------------------------------------------|
| Register                                             |
|                                                      |
| Username: [       ]                                  |
| Password: [       ]                                  |
| Email:    [       ]                                  |
| Role:     [Drop-Down Menu (Student, Teacher, Admin   |
|           Moderator)]                                |
|                                                      |
| [Register]                                           |
|                                                      |
| Already have an account? Log in!                     |
+------------------------------------------------------+
```

## Route Parameters:

None

## Query Parameters:
None

## Link Destinations for Page

**Submit success** → `/login` (redirect)
**Submit failure** → `/register` (show Register page with error message)

## Data Required to Render Page

1. UI state: username, password, email, role, validation errors
2. API: To be added
3. Auth State Storage: To be added

## Tests for Verifying Rendering of the Page

1. **Template elements rendered**
   - Page title is displayed
   - Page header is displayed
   - Username, Password, Email, Role entry fields are visible, user can enter data
   - Role drop-down menu is visible, menu items are clickable
   - Register button is visible and clickable
   - Link to Login page is visible and clickable
   - Error messages are visible if attempted user credentials are   invalid (attempted credentials do not meet validation parameters, account with attempted username and/or email already exists)


2.   **Redirect Behaviour**
   - If user credentials are valid, redirect to Login page
   - If user is in session, redirect to Dashboard page

# 3) Dashboard Page

## Page Title
Dashboard

## Page Description
This is the home page displayed after a user logs in. It allows users to view posts, interact with posts, or create a new post.

## Page Route
**Dashboard →** `/dashboard`

## Mockup for Dashboard
![Dashboard](Dashboard.png)

## Route Parameters
Login → Dashboard  
Users must be logged in to access the dashboard.

## Query Parameters
None

## Link Destinations for Page
`/dashboard`

## Data Required to Render Page
- Comments
- Files
- User-created posts

## Tests for Verifying Rendering of the Page
- Render posts stored in the database.
- Render comments stored in the database.


# 4) Create Post Page

## Page Title
Create Post

## Page Description
Allows a user to create a post with a title, description, file upload, and category.

## Page Route
`/create_post`

## Mockup for Create Post
![View_A_Post](View_A_Post.png)

## Route Parameters
User must be logged in.

## Query Parameters
- Query posts and files
- Query categories
- Query comments

## Link Destinations for Page
- Back to dashboard
- Submit post

## Data Required to Render Page
- Categories defined in the database
- Comments and files associated with the post in the database

## Tests for Verifying Rendering of the Page
- Verify title input is required
- Verify description input is required


# 5) View Single Post Page

## Page Title
Varies – defined by user input (post title)

## Page Description
Allows a user to view another user’s post and interact with it (e.g., view files and comments).

## Page Route
`/create_post`

## Mockup for View All Posts
![View_A_Post](View_A_Post.png)

## Route Parameters
User must be logged in.

## Query Parameters
- Files and comments retrieved from the database
- User hash keys for comments

## Link Destinations for Page
Back to dashboard

## Data Required to Render Page
- Files associated with the post
- Comments associated with the post
- User hash keys for comment authors

## Tests for Verifying Rendering of the Page
- Verify the file displays correctly
- Verify username hashes display correctly
- Verify comments render correctly

