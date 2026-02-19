# Milestone 1: Project Proposal

## Project Title: AnonReview

### Team Information
* Team Number: 3
* Team Name: HomeworkBusters

### Team Members
* Faisal Shahin - faisal.shahin@colorado.edu GitHub: shahinfa9999
* Adeline Bowman - adbo5692@colorado.edu GitHub: Adeline-Bowman
* Nicholas Woody - niwo9128@colorado.edu GitHub: niwo91
* Nandini Bhat - nandini.bhat@colorado.edu, GitHub: nabhCO

### Scheduled Weekly Team Meeting
Mondays at 7 PM via zoom

### Vision Statement
AnonReview is a web-based peer review platform that allows students to anonymously submit homework and exam related content for feedback. Submissions can include written responses, code snippets, and PDF documents. The platform supports inline comments and small group review so students can receive targeted help and collaborate with peers in a low pressure environment.

### Motivation
With online schooling becoming more prevelant, we felt like something missing was the huddling outside of class to talk about homework or exam answes. Students often struggle to get meaningful feedback on partial solutions, written work, or code outside of office hours. Many existing discussion tools are not designed for structured peer review or document annotation. 
AnonReview aims to provide a dedicated space where students can share work anonymously and receive constructive feedback to help them improve their understanding.

### Risks to Project Completion
* Academic integrity concerns may arise if students attempt to share full solutions to active assignments or exams.
* Supporting file uploads and inline annotations may introduce technical complexity.
* Implementing breakout group collaboration features may be challenging within the semester timeline.
* Getting adequate data for testing.
* Technical challenges include learning many new skills. 

### Mitigation Strategy
* Have different user permission levels to enable moderation of content.
  * The platform will include clear guidelines to discourage posting full solutions for active assessments and will emphasize conceptual feedback.
* Development will follow an Minimum Viable Product(MVP) first approach, with basic submission and review functionality implemented before more advanced features.
  * File uploads and inline comments will be prioritized, while breakout group collaboration will be treated as a stretch goal if time permits.
* We could create our own data or take examples from online resources for input.
  * Uploading assignments from previous classes.
* We will apply the material we've learned in class and use online documentation.

### Development Method
* The team will follow an Agile, sprint based development process with weekly planning meetings and short development iterations.
  * Sprints will be 1 week long.
* Features will be implemented incrementally, with regular integration and testing to reduce risk.
* We'll have unit tests as part of our acceptance criteria.

## Development Steps (Epics)

#### Epic 1: User Accounts and Anonymous Identity  
**Goal:** Allow users to create accounts and participate anonymously while preserving internal identity mapping.

**Stories:**  
- As a user, I can register and log in.  
- As a user, I can post content anonymously.  
- As a system, I can map anonymous posts to real users internally without exposing identities to others.  

**Deliverables:**  
- User authentication system  
- Anonymous identity mapping in backend  
- Account creation and login UI  

---

#### Epic 2: Multi Format Submissions  
**Goal:** Support multiple submission formats for homework and exam content.

**Stories:**  
- As a user, I can submit text-based questions and explanations.  
- As a user, I can upload code snippets with syntax highlighting.  
- As a user, I can upload PDF documents for review.  

**Deliverables:**  
- Submission schema for text, code, and PDFs  
- File upload and storage endpoints  
- Frontend submission UI with syntax highlighting support  

---

#### Epic 3: Inline Review and Annotations  
**Goal:** Enable contextual feedback directly on submissions.

**Stories:**  
- As a reviewer, I can leave line-by-line comments on code snippets.  
- As a reviewer, I can leave section-level comments on PDF documents.  
- As a user, I can view and reply to threaded discussions tied to specific annotations.  

**Deliverables:**  
- Annotation data model  
- Inline commenting API  
- Frontend annotation and threaded discussion UI  

---

#### Epic 4: Peer Review and Feedback  
**Goal:** Encourage meaningful feedback and peer learning.

**Stories:**  
- As a user, I can comment on submissions.  
- As a user, I can upvote helpful feedback.  
- As a user, I can build reputation based on peer feedback (optional).  

**Deliverables:**  
- Comment and feedback endpoints  
- Upvote system  
- Basic reputation scoring logic and UI  

---

#### Epic 5: Breakout Review Groups  
**Goal:** Support small-group collaborative reviews.

**Stories:**  
- As a user, I can create or join a small review group for a submission.  
- As a group, we can discuss a submission in a shared thread.  
- As a group, we can generate a summarized group feedback response.  

**Deliverables:**  
- Group model and membership endpoints  
- Group discussion threads  
- Group feedback summary view  

---

#### Epic 6: Moderation and Reporting  
**Goal:** Maintain platform quality and academic integrity.

**Stories:**  
- As a user, I can flag inappropriate or integrity-violating content.  
- As a moderator, I can review and act on reported content.  
- As a moderator, I can manage flagged submissions and comments.  

**Deliverables:**  
- Reporting system and flag schema  
- Moderator dashboard  
- Basic moderation actions (review, hide, remove)  
---

## Project Tracking
The team will use Trello to track tasks, sprint progress, and blockers. Tasks will be assigned to individual team members and prioritized during weekly planning meetings. [Link to our tracking software page](https://team-3-project.atlassian.net/jira/core/projects/T3/board)

## Technology Stack

### Frontend
-React with TypeScript for building the user interface
-HTML and CSS for layout and styling

### Backend
-Python with Flask for REST API development

### Database
-SQLite for local development
-PostgreSQL for deployment or production use

### File Storage
-Local file storage during development
-Cloud object storage for deployment if needed

### Sample User Stories

As a student, I want to anonymously upload a code snippet so others can comment on specific lines and help me debug.
As a student, I want to upload a PDF of my written homework so reviewers can leave comments on particular sections.
As a student, I want to join a small review group to discuss an assignment with other students.
As a reviewer, I want to leave inline comments on specific lines of code so my feedback is clear and targeted.
As a reviewer, I want to annotate sections of a PDF to point out conceptual mistakes.
As a moderator, I want to flag or remove posts that violate academic integrity guidelines.











