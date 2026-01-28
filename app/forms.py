# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SuggestionForm(FlaskForm):
    category = SelectField('Category', validators=[DataRequired()])
    content = TextAreaField('Suggestion', validators=[
        DataRequired(),
        Length(min=10, max=2000, message='Suggestion must be between 10 and 2000 characters')
    ])
    is_anonymous = BooleanField('Submit Anonymously', default=True)
    personnel_number = StringField('Personnel Number', validators=[
        Optional(),
        Length(min=5, max=20, message='Personnel number must be between 5 and 20 characters')
    ])
    submit = SubmitField('Submit Suggestion')

    def validate_personnel_number(self, field):
        if not self.is_anonymous.data and not field.data:
            raise ValidationError('Personnel number is required when not submitting anonymously')