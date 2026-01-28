# app/utils.py
from functools import wraps
from flask import abort
from flask_login import current_user


def requires_role(allowed_roles):
    """
    Decorator to restrict access to routes based on user roles.

    Args:
        allowed_roles (list): A list of roles that are allowed to access the route.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Reason: Check if the user is authenticated and their role is in the list of allowed roles
            if not current_user.is_authenticated or current_user.role not in allowed_roles:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def get_categories():
    """Return the list of predefined categories for AFCSC."""
    return [
        "Department of Land Warfare",
        "Department of Maritime Warfare",
        "Department of Air Warfare",
        "Academics & Research",
        "Facilities & Maintenance",
        "Feeding & Messing",
        "Administration & Policies",
        "Health & Safety",
    ]


def validate_category(category):
    """Validate if a category is in the predefined list."""
    return category in get_categories()
