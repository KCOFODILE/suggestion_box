import sys
from getpass import getpass
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Create Flask app context
app = create_app()
app.app_context().push()


def create_user():
    """
    Creates a new user in the database via command line.
    Prompts for username, password, and role.
    """
    print("--- Create New User ---")

    username = input("Enter username: ")
    if not username:
        print("Username cannot be empty.")
        sys.exit(1)

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"Error: User '{username}' already exists.")
        sys.exit(1)

    password = getpass("Enter password: ")
    if not password:
        print("Password cannot be empty.")
        sys.exit(1)

    confirm_password = getpass("Confirm password: ")
    if password != confirm_password:
        print("Passwords do not match.")
        sys.exit(1)

    print("\nAvailable roles: admin_full, admin_view_only, viewer")
    role = input("Enter role (default: admin_view_only): ").strip().lower() or "admin_view_only"

    allowed_roles = ["admin_full", "admin_view_only", "viewer"]
    if role not in allowed_roles:
        print(f"Error: Invalid role '{role}'. Allowed roles are: {', '.join(allowed_roles)}")
        sys.exit(1)

    try:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password, role=role)

        db.session.add(new_user)
        db.session.commit()

        print(f"\nUser '{username}' with role '{role}' created successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"\nError creating user: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_user()
