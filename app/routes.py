# app/routes.py
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, Response, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Suggestion
from app.forms import LoginForm, SuggestionForm
from app.utils import requires_role, get_categories
from urllib.parse import urlparse
import logging
import os
from flask import current_app

main_bp = Blueprint("main", __name__)
log = logging.getLogger(__name__)


@main_bp.route("/admin/download-db")
def download_db():
    token = request.args.get("token")
    if not token or token != current_app.config.get("DOWNLOAD_TOKEN"):
        log.warning(f"Unauthorized DB download attempt from {request.remote_addr}")
        return "Unauthorized", 403
    
    db_path = os.path.join(current_app.root_path, "..", "suggestion_box.db")
    if os.path.exists(db_path):
        return send_file(db_path, as_attachment=True)
    else:
        return "Database file not found", 404


@main_bp.route("/")
def index():
    # if current_user.is_authenticated:
    #     return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "danger")
            return redirect(url_for("main.login"))

        login_user(user)
        next_page = request.args.get("next")
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("main.dashboard")
        flash("Login successful!", "success")
        return redirect(next_page)

    return render_template("login.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


@main_bp.route("/submit-suggestion", methods=["GET", "POST"])
def submit_suggestion():
    form = SuggestionForm()
    form.category.choices = [(cat, cat) for cat in get_categories()]

    if form.validate_on_submit():
        try:
            suggestion = Suggestion(
                content=form.content.data,
                category=form.category.data,
                is_anonymous=form.is_anonymous.data,
                submitter_personnel_number=None if form.is_anonymous.data else form.personnel_number.data,
            )
            db.session.add(suggestion)
            db.session.commit()
            flash("Your suggestion has been submitted successfully!", "success")
            return redirect(url_for("main.index"))
        except Exception as e:
            db.session.rollback()
            log.error(f"Error submitting suggestion: {e}", exc_info=True)
            flash("An error occurred while submitting your suggestion. Please try again.", "danger")

    return render_template("submit_suggestion.html", form=form)


@main_bp.route("/dashboard")
@login_required
@requires_role(["admin_full", "admin_view_only"])
def dashboard():
    category = request.args.get("category")
    query = Suggestion.query.order_by(Suggestion.timestamp.desc())

    if category:
        query = query.filter_by(category=category)

    suggestions = query.all()
    categories = get_categories()
    user_role = current_user.role

    if request.headers.get("HX-Request"):
        return render_template(
            "_suggestions_list_content.html",
            suggestions=suggestions,
            role=user_role,
        )
    else:
        return render_template(
            "dashboard.html",
            suggestions=suggestions,
            categories=categories,
            selected_category=category,
            role=user_role,
        )


@main_bp.route("/delete_suggestion/<int:suggestion_id>", methods=["POST"])
@login_required
@requires_role("admin_full")
def delete_suggestion(suggestion_id):
    suggestion = Suggestion.query.get_or_404(suggestion_id)

    try:
        db.session.delete(suggestion)
        db.session.commit()
        log.info(f"Suggestion {suggestion_id} deleted by user {current_user.username}")
        flash("Suggestion deleted successfully.", "success")
        if request.headers.get("HX-Request"):
            return Response(status=200)
    except Exception as e:
        db.session.rollback()
        log.error(f"Error deleting suggestion {suggestion_id}: {e}", exc_info=True)
        flash(f"Error deleting suggestion: An internal error occurred.", "danger")
        if request.headers.get("HX-Request"):
            response = Response("Error deleting suggestion", status=500)
            response.headers["HX-Trigger"] = '{"showError": "Failed to delete suggestion"}'
            return response

    return redirect(url_for("main.dashboard"))


@main_bp.route("/api/suggestions")
@login_required
@requires_role(["admin_full", "admin_view_only"])
def get_suggestions():
    category = request.args.get("category")
    query = Suggestion.query.order_by(Suggestion.timestamp.desc())

    if category:
        query = query.filter_by(category=category)

    suggestions_data = [suggestion.to_dict() for suggestion in query.all()]
    return jsonify(suggestions_data)


@main_bp.route("/api/suggestion/<int:id>", methods=["PUT"])
@login_required
@requires_role(["admin_full", "admin_view_only"])
def update_suggestion_status(id):
    suggestion = Suggestion.query.get_or_404(id)
    new_status = request.form.get("status")

    valid_statuses = ["New", "In Progress", "Resolved", "Rejected"]

    if not new_status or new_status not in valid_statuses:
        log.warning(f"Invalid status update attempt for suggestion {id}: {new_status}")
        return Response("Error: Invalid status value.", status=400)

    if suggestion.status == new_status:
        return render_template("_suggestion_select.html", suggestion=suggestion, role=current_user.role)

    try:
        suggestion.status = new_status
        db.session.commit()
        log.info(f"Suggestion {id} status updated to '{new_status}' by {current_user.username}")
        return render_template("_suggestion_select.html", suggestion=suggestion, role=current_user.role)
    except Exception as e:
        db.session.rollback()
        log.error(f"Error updating status for suggestion {id}: {e}")
        response = Response("Error: Server error during update.", status=500)
        response.headers["HX-Trigger"] = '{"showError": "Failed to update status"}'
        return response

    except Exception as e:
        db.session.rollback()
        log.error(f"Database error updating status for suggestion {id}: {e}", exc_info=True)
        response = Response("Error: Could not update status due to server error.", status=500)
        response.headers["HX-Trigger"] = '{"showError": "Failed to update status"}'
        log.debug(f"--- PUT /api/suggestion/{id} End (500 - DB Error) ---")
        return response
