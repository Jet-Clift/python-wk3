from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired()])
    password = StringField("Password", [validators.InputRequired()])
    