from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from app import authentication as at, login_manager
from app.models.users import Users
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# login form
class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField('Password', validators=[DataRequired()]) 
    stay_logged_in = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    
#login route
@at.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    return render_template("auth/login.html", form = form)