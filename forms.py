'''Module for storing any forms we may create. For now just login and registration, maybe
for creating posts and file uploads later on?'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

'''Creating the LoginForm and RegistrationForm classes with fields for data entry
Variables:
user_name (input type=string, data entry required for form submission)
password (input type=password, data entry required for form submission, minimum length 10)
submit (type=button, allows user to submit info they've entered for login or registration)
'''
class LoginForm(FlaskForm):

    user_name = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=10, message="Password is too short")])
    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):

    user_name = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=10, message="Password is too short")])
    submit = SubmitField("Register")

