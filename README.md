Milestone 1: Project Proposal

Project Title
AnonReview

Team Information
Team Number: 3
Team Name: TBD / HomeworkBusters

Team Members
Faisal Shahin
Adeline Bowman
Nicholas Woody
Nandini Bhat

Scheduled Weekly Team Meeting
Mondays at 7 PM via zoom

Vision Statement
AnonReview is a web-based peer review platform that allows students to anonymously submit homework and exam related content for feedback. Submissions can include written responses, code snippets, and PDF documents. The platform supports inline comments and small group review so students can receive targeted help and collaborate with peers in a low pressure environment.

Motivation
With online schooling becomign more prevelant, we felt like something missing was the huddling outside of class to talk about homework or exam answes. Students often struggle to get meaningful feedback on partial solutions, written work, or code outside of office hours. Many existing discussion tools are not designed for structured peer review or document annotation. 
AnonReview aims to provide a dedicated space where students can share work anonymously and receive constructive feedback to help them improve their understanding.

Risks to Project Completion
Academic integrity concerns may arise if students attempt to share full solutions to active assignments or exams. Supporting file uploads and inline annotations may introduce technical complexity. Implementing breakout group collaboration features may be challenging within the semester timeline.
Getting adequate data.
Technical changess include learning many new skills. 

Mitigation Strategy
The platform will include clear guidelines to discourage posting full solutions for active assessments and will emphasize conceptual feedback. Development will follow an MVP first approach, with basic submission and review functionality implemented before more advanced features. File uploads and inline comments will be prioritized, while breakout group collaboration will be treated as a stretch goal if time permits.

Development Method
The team will follow an Agile, sprint based development process with weekly planning meetings and short development iterations. Features will be implemented incrementally, with regular integration and testing to reduce risk.

Development Steps

1. Define user roles, anonymity model, and supported content types such as text, code, and PDF.
2. Design database schema for users, posts, attachments, comments, and review groups.
3. Implement backend API endpoints for submissions, file uploads, inline comments, and moderation.
4. Build frontend views for posting content, viewing submissions, and adding line specific feedback.
5. Implement breakout group review workflows if time permits.
6. Integrate frontend and backend and conduct usability testing.
7. Prepare final documentation and project demo.

Project Tracking
The team will use  Trello to track tasks, sprint progress, and blockers. Tasks will be assigned to individual team members and prioritized during weekly planning meetings.

Technology Stack

Frontend
React with TypeScript for building the user interface
HTML and CSS for layout and styling

Backend
Python with Flask for REST API development

Database
SQLite for local development
PostgreSQL for deployment or production use

File Storage
Local file storage during development
Cloud object storage for deployment if needed

Epics

Epic 1: User accounts and anonymous identity
Account registration and login
Anonymous posting system
Internal identity mapping not visible to other users

Epic 2: Multi format submissions
Text based questions and explanations
Code snippet uploads with syntax highlighting
PDF document uploads

Epic 3: Inline review and annotations
Line by line comments on code snippets
Section level comments on PDF documents
Threaded discussions on specific annotations

Epic 4: Peer review and feedback
Commenting and feedback threads
Upvoting helpful feedback
Optional reviewer reputation system

Epic 5: Breakout review groups
Create small review groups for a submission
Group discussion threads
Group based feedback summaries

Epic 6: Moderation and reporting
Flagging inappropriate or integrity violating content
Moderator dashboard for reviewing reports

Sample User Stories

As a student, I want to anonymously upload a code snippet so others can comment on specific lines and help me debug.
As a student, I want to upload a PDF of my written homework so reviewers can leave comments on particular sections.
As a student, I want to join a small review group to discuss an assignment with other students.
As a reviewer, I want to leave inline comments on specific lines of code so my feedback is clear and targeted.
As a reviewer, I want to annotate sections of a PDF to point out conceptual mistakes.
As a moderator, I want to flag or remove posts that violate academic integrity guidelines.


