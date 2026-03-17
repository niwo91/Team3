## WEEKLY_STATUS.md
### Project Milestone 3: Weekly Status Report
**Project:** AnonReview
**Team Number:** 3
**Team Name:** AnonReview
---
### Reporting Period
**Week:** 3
**Meeting Held:** 
**Meeting Date:** March 2nd, 2026
**Meeting Duration: 40 minutes** 
**Meeting Format:** Zoom
---
### Overview
This captures the **Weekly Status** of the AnonReview project.
It is intended to provide a concise snapshot of progress, plans, and risks, and
will be updated weekly throughout the project.
This weekly status format is designed to:
- Track ongoing progress over time
- Surface risks and blockers early
- Provide accountability for individual contributions
- Supplement the project management tool used by the team
---
### Project Management Snapshot
The Team is using Trello(jira) to track [project status](https://team-3-project.atlassian.net/jira/core/projects/T3). The team has tasks which are assigned and moved to a "done" status when complete
---
### Progress Since Last Week
* Basic website styling
* Uploaded files viewable
* Tested Database connection, created dynamic page for categories
* Created login form
* Created Registration form
* Created test data in database
---
### Completed Tasks
* Website styling
---
### Planned Tasks for Next Week
* Connect login and registration to database
* Navigation flow of website
* Anonymity of users (Anonymous posts and comments)
* Get uploaded documents viewable on a web page
* Allow comments
---
### Blockers and Issues
* Password length needs to be 10 characters long
* Database connection
* Module for routes
---
### Risks and Mitigation
**Identified Risk: Potential clashes with merging**
- Mitigation: Seperate basic_app.py into multiple files
**Identified Risk: integration sprawl**
- Mitigation: Focusing solely on epic 1
---
### Team Reflection
* Focusing on finishing epic 1 so we can have an MVP
* Mid-week check-in was a good addition
* Understanding the navigation of the website
---
### Individual Contributions This Week
- Nandini: looked into extensions to make logins and registration easier. Created login forms. Created login and registration pages. Created secret key for .env (stored locally).
- Nick: Created a dynamic page that shows the post categories pulled from the database.
- Faisal: Made uploaded files viewable. Created CSS file. Added flags for database when database is up.
- Adeline: Made test cases for the database, test posts, test user for each of the different permission levels. Looked into Google Auth.
---
### Notes
This file will be updated weekly as the project progresses. Earlier weekly entries may be retained below or moved to an archive directory if
the file grows large.
---
### Reporting Period
**Week:** 3
**Meeting Held:** 
**Meeting Date:** March 9th, 2026
**Meeting Duration: 40 minutes** 
**Meeting Format:** Zoom

### Progress Since Last Week
* Log in and register functionality
* Dashboard
* Comment functionality
* files viewable in HTML
---
### Completed Tasks
* Log in and register functionality
* Dashboard
* Comment functionality
* files viewable in HTML
---
### Planned Tasks for Next Week
* Work on authentication. Flask log in extension based work. 
* Improve website navigation. 
* Updating file path to a file section. 
* TO DO FS 
---
### Blockers and Issues
* Lack of posts.
* Database planning.
---
### Risks and Mitigation
**Identified Risk: Clashes with merging**
- Mitigation: Seperate basic_app.py into multiple files
**Identified Risk: Database connectivity**
- Mitigation: Finalize database structure. Upload files into the database. 
---
### Team Reflection
* Better communicated branch and merge.
* Epic one is done.
---
### Individual Contributions This Week
- Nandini: Log in and registration functionality. Finished connecting log in and connection to database. Updated registration fields to connect to database.
- Nick: Created a basic comment section, comments upload to database. Basic implementation since no post id's are intigrated with the database yet. 
- Faisal: Broke up the uploaded files into html text so it is interactable. Started conecctino to database but not fully tested.  
- Adeline: Created the ananomizer function. Made a post section to connect to comments, files, and dashboard. Not fully tested, block until team commits are done. 
---
### Notes
This file will be updated weekly as the project progresses. Earlier weekly entries may be retained below or moved to an archive directory if
the file grows large.
----
### Reporting Period
**Week:** 4
**Meeting Held:** 
**Meeting Date:** March 16th, 2026
**Meeting Duration: 40 minutes** 
**Meeting Format:** Zoom

### Progress Since Last Week/Completed Tasks
- Created user sessions for login. Implemented restricted views based off the login session. Session timeout (60mins).Combined upload file route, view post route with the create post route and view file route. Created the delete post functionality, connected file names to database. Created the filter buttons, moved delete post to post view page and added deletion permissions.
---
### Planned Tasks for Next Week
- Nandini - Add a hashing function for the password. Will add new users with new passwords.
- Nick - Files to blobs and storing them in SQLite as blobs. Update User table with active/inactive bool. Delete extra code.
- Faisal - Create inline comments and upvote and downvote functionality.
- Adeline - Fix the new post page. Make a user profile page for updates.
---
### Blockers and Issues
* Lack of posts.
* Database planning.
---
### Risks and Mitigation
**Identified Risk:Anyone could delete posts**
- Mitigation: User priviliges. 
**Identified Risk:Overwriting files with current implementation**
- Mitigation: Storing files as blobs.
**Identified Risk:Lots of people working on DB file at the same time**
- Mitigation: Communication
---
### Team Reflection
* We've made a lot of progress with the app.
---
### Individual Contributions This Week
- Nandini: Created user sessions for login. Implemented restricted views based off the login session. Session timeout (60mins).
- Nick: Combined upload file route, view post route with the create post route and view file route.
- Faisal: Created the delete post functionality, connected file names to database
- Adeline: Created the filter buttons, moved delete post to post view page and added deletion permissions.
---
