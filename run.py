# run.py
from app import create_app, db
from app.models import User
import click
from flask.cli import with_appcontext

app = create_app()


@app.cli.command("create-viewer")
@click.argument("username")
@click.argument("password")
def create_viewer(username, password):
    """Create a viewer user."""
    try:
        user = User(username=username, role="viewer")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Created viewer user: {username}")
    except Exception as e:
        click.echo(f"Error creating user: {e}")
        db.session.rollback()


@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    try:
        db.create_all()
        click.echo("Database tables created successfully")
    except Exception as e:
        click.echo(f"Error creating database tables: {e}")


if __name__ == "__main__":
    app.run(debug=True)
