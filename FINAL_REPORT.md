# Homework Busters Final Report
## Milestone 8: Final Report Submission
## Project Title
AnnonReview - A Collaborative Study Group Coordination Platform
## Team Members
- Faisal Shahin
- Adeline Bowman
- Nicholas Woody
- Nandini Bhat
## Required Links
- Project tracker (instructor can access): [Trello
Board](https://team-3-project.atlassian.net/jira/core/projects/T3/board?filter=&groupBy=status)
- Version control repository (instructors have access): [GitHub
Repo](https://github.com/niwo91/Team3)
- 5-minute customer demo video: [Demo Video](https://youtu.be/dShZ4i4XUP0)
- Public deployment site: [StudySync Deployment](https://team3-qcsm.onrender.com)
## Repository Readiness
All team members have verified that their latest work is pushed to the remote
repository.
The repository contains the following required files and assets:
- README.md
- WEEKLY_STATUS.md
- PAGE_TESTING.md
- SQL_TESTING.md
- FINAL_REPORT.md
- Project presentation files from the Presentation Milestone -- NEED TO ADD
- Video of demo -- NEED TO ADD
- Source code (frontend and backend)
- Test cases (unit and integration)
- Source documentation and auto-generated documentation files
## Final Status Report
### What We Completed
- Full authentication system with login, registration, and session management using Flask-Login
- Role-based access control (student, teacher, admin, moderator)
- Post creation with optional file uploads (text, code, PDF, HTML, DOCX)
- Anonymous posting system using generated pseudonyms
- Commenting system with optional line-level annotations for uploaded files
- Upvote and downvote system for comments with duplicate prevention
- Reporting system for posts and comments, including moderation workflow
- Admin and moderator dashboard for reviewing reports
- Category-based organization of posts including a dedicated "Reported Items" category
- PostgreSQL and SQL-ite database with relational schema and constraints
- Deployment on Render with persistent database
### What We Were in the Middle of Implementing
- Real-time updates for comments and reports (currently request-based refresh)
- Improved UI consistency and layout spacing
- Better file preview support for additional formats
- Expanded automated testing coverage
- Break out rooms Epic
### What We Planned for the Future
- WebSocket-based real-time updates for comments and moderation
- Improved UI/UX and mobile responsiveness
- Rich text editor for posts and comments
- Advanced moderation tools (bulk actions, filters)
- Notifications system for replies and reports
- Integration with external tools like Google Docs or GitHub
- More advanced scheduling preferences
- Breakout room Epic
### Known Problems and Limitations
- No real-time updates, relies on page refresh
- File preview support is limited for some formats like .doc
- Moderation system is functional but basic
- Limited automated testing and edge case coverage
- UI is functional but not fully polished
## System Overview
AnonReview follows a standard web application architecture:

- Backend: Flask application handling routing, authentication, and business logic
- Database: PostgreSQL accessed through psycopg2 with helper query functions, and SQL Lite
- Frontend: HTML templates rendered with Jinja2
The system was designed to support incremental development, clear separation of
concerns, and straightforward testing.

Key design decisions:
- Separation of concerns using a methods.py file for database logic
- Use of Flask-Login for session and authentication management
- Binary storage of uploaded files directly in the database
- Role-based authorization enforced at route level

## Page Data Access Tests (High-Level)

### Use case name
Create post with file upload

### Description
Verify that a logged-in user can create a post with an attachment and that the file is stored and retrieved correctly.

### Pre-conditions
- User account exists
- User is logged in
- Valid file type is selected

### Test steps
1. Navigate to create post page
2. Enter title and body
3. Upload a valid file
4. Submit form
5. Open created post

### Expected result
- Post is created successfully
- File is stored as a binary blob
- File content is displayed correctly depending on type

### Actual result
- Post is created and file is displayed correctly

### Status
Pass

### Notes
File preview depends on file type support

### Post-conditions
- New post is stored in database with attachment


## Reflection

This project gave us experience building a full-stack web application from scratch.

### Key takeaways
- Separating database logic from routes made development easier to manage
- Starting with a simple schema and iterating helped avoid major redesigns
- Authentication and role management added significant complexity but improved realism
- Deployment early helped catch environment and database issues
- Working with file uploads and binary storage introduced practical challenges

Overall, we successfully built a functional anonymous review platform with moderation features and a scalable foundation for future improvements.
