# app/models.py
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='viewer')
    appointment = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_anonymous = db.Column(db.Boolean, default=True, nullable=False)
    submitter_personnel_number = db.Column(db.String(20))
    status = db.Column(db.String(20), default='New')

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'category': self.category,
            'timestamp': self.timestamp.isoformat(),
            'is_anonymous': self.is_anonymous,
            'submitter': 'Anonymous' if self.is_anonymous else self.submitter_personnel_number,
            'status': self.status
        }