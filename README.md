# Suggestion Box App

This is a web application for submitting and viewing suggestions and complaints for an online school.

## Features

- Modern, militaristic-themed user interface
- Student suggestion submission (anonymous or with personnel number)
- Categorization of suggestions
- Secure login for authorized personnel (viewers)
- Dashboard to view and filter suggestions by category, with color-coded status indicators
- Role-based access control for viewing and deleting suggestions

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd suggestion-box
    ```
2.  **Install dependencies and create virtual environment:**
    ```bash
    uv sync
    ```
3.  **Set up the database:**
    ```bash
    uv run flask db upgrade
    ```
4.  **Create a user:**
    ```bash
    uv run python create_user.py
    ```
    Follow the prompts to create a user with the desired role (admin_full, admin_view_only, or viewer).

5.  **Run the application:**
    ```bash
    uv run flask run
    ```

The application will be available at `http://127.0.0.1:5000/`.

## Project Structure

- `app/`: Contains the main application code
    - `__init__.py`: Application factory
    - `forms.py`: Flask-WTF forms
    - `models.py`: SQLAlchemy models
    - `routes.py`: Flask routes
    - `utils.py`: Utility functions
    - `templates/`: HTML templates
- `migrations/`: Alembic migration scripts
- `docs/`: Project documentation (`PLANNING.md`, `TASK.md`)
- `envbot/`: Python virtual environment
- `requirements.txt`: Project dependencies
- `run.py`: Script to run the Flask application
- `create_user.py`: Script to create application users
- `config.py`: Application configuration
- `suggestion_box.db`: SQLite database file (for development)

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Migrate
- WTForms
- Jinja2
- HTMX
- Tailwind CSS (via CDN in templates)

## Contributing

(Add contributing guidelines here if applicable)

## License

(Add license information here if applicable)
