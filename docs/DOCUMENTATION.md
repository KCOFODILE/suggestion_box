# Project Documentation: Suggestion Box App

## 1. Project Overview
The **Suggestion Box App** is a specialized web platform designed for an online school environment. It serves as a secure, role-based channel for students to submit suggestions or complaints and for authorized personnel to manage, track, and resolve these entries. The application features a distinctive "militaristic" aesthetic, emphasizing order, clarity, and security.

## 2. Purpose & Value Proposition
- **Anonymous Feedback:** Encourages honest student input by offering anonymity while providing an option for identified submissions via personnel numbers.
- **Efficient Management:** Provides a centralized dashboard for administrators to filter, monitor, and update the status of suggestions.
- **Ordered Communication:** Categorizes input (Academics, Facilities, etc.) to ensure the right departments receive relevant feedback.
- **Role-Based Security:** Protects sensitive data through granular access controls (Full Admin vs. View-Only).

## 3. System Architecture
The application is built on a modern Python web stack:
- **Backend:** [Flask](https://flask.palletsprojects.com/) (Web Framework)
- **Database:** [SQLAlchemy](https://www.sqlalchemy.org/) ORM with [SQLite](https://www.sqlite.org/) (for development) and [Flask-Migrate](https://flask-migrate.readthedocs.io/) for schema versioning.
- **Authentication:** [Flask-Login](https://flask-login.readthedocs.io/) manages user sessions and role-based access.
- **Frontend:** [Jinja2](https://jinja.palletsprojects.com/) templates styled with [Tailwind CSS](https://tailwindcss.com/) (via CDN) and enhanced with [HTMX](https://htmx.org/) for dynamic, AJAX-like interactions without full page reloads.

### Data Model
- `User`: Handles authentication and roles (`admin_full`, `admin_view_only`, `viewer`).
- `Suggestion`: Stores feedback content, category, timestamp, anonymity status, and current resolution state (`New`, `In Progress`, `Resolved`, `Rejected`).

## 4. Process & Data Flows
### Suggestion Submission Flow
1. **Trigger:** Student visits the "Submit Suggestion" page.
2. **Processing:** Input is validated (length, required category). If non-anonymous, personnel number is required.
3. **Storage:** Entry is saved to the SQLite database with a `New` status.
4. **Response:** Success message via Flask's flash system; user redirected to home.

### Admin Management Flow
1. **Trigger:** Admin logs in and accesses the "Dashboard".
2. **Filtering:** Admin selects a category. **HTMX** intercepts the change, fetches the filtered fragment, and updates the UI without a reload.
3. **Status Update:** Admin changes a suggestion's status via a dropdown. **HTMX (PUT request)** updates the backend and refreshes the specific row.
4. **Deletion:** `admin_full` users can delete entries, which triggers a database removal and UI refresh.

## 5. UX Flows & User Journeys
### The Student Journey
- **Intent:** Provide feedback without fear of reprisal.
- **Touchpoint:** Minimalist home page → Submission Form.
- **Experience:** High-contrast, dark-mode UI ("militaristic") provides a sense of officiality and security.

### The Admin Journey
- **Intent:** Quickly identify and manage urgent issues.
- **Touchpoint:** Login → Dashboard.
- **Experience:** Color-coded status badges and real-time filtering allow for rapid scanning of school-wide feedback.

## 6. UI & Component Intent
- **Militaristic Theme:** Uses deep grays (`zinc-800`), greens (`green-800`), and high-contrast text to evoke a professional, disciplined environment.
- **Status Badges:** Visual indicators (Blue for New, Yellow for Progress, Green for Resolved) provide immediate cognitive feedback on resolution progress.
- **HTMX Selectors:** Used for seamless status transitions, reducing friction in administrative tasks.
- **Responsive Cards:** On mobile, the suggestion table transforms into a vertical card layout to maintain readability on small screens.

## 7. Folder & File Responsibilities
- `app/`: Core application logic.
    - `__init__.py`: Factory function and extension initialization.
    - `models.py`: Database schema definitions.
    - `routes.py`: Endpoint logic and role-based protection.
    - `forms.py`: Server-side input validation.
    - `utils.py`: Helpers (decorators for roles, category lists).
    - `templates/`: Jinja2 templates (layouts and fragments).
- `migrations/`: History of database schema changes.
- `docs/`: Supplemental documentation and planning files.
- `run.py` & `main.py`: Entry points for launching the dev server.
- `create_user.py`: CLI utility for managing administrative accounts.

## 8. Design & UX Philosophy
- **"Form Follows Function":** The UI is utilitarian; every element serves a purpose in the feedback lifecycle.
- **Security-First:** Non-authenticated users can only submit; they cannot view any data.
- **Partial Page Updates:** Prioritizes speed and responsiveness through HTMX fragments (`_suggestions_list_content.html`).

## 9. Risks, Assumptions & Knowledge Gaps
- **Scaling:** SQLite is used for development; production deployment may require PostgreSQL/MySQL.
- **Security:** Static CSS/JS via CDN depends on external availability and carries minor security implications (SRI recommended).
- **Session Management:** Default Flask session handled via cookies; ensure `SECRET_KEY` is rotated in production.

## 10. Onboarding Guide (How to Get Productive Fast)
1. **Setup Env:** Use `uv run` or standard `venv` + `pip install -r requirements.txt`.
2. **DB Init:** Run `flask db upgrade` to create the schema.
3. **User Creation:** Use `python create_user.py` to create an `admin_full` account.
4. **Local Run:** Start the server with `python run.py`.
5. **Logic Location:** New features should generally involve `models.py` (data), `routes.py` (logic), and `templates/` (UI).
