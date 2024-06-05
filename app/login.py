from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from app import login, create_app
from app.models.users import Users
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user

bcrypt = Bcrypt()
login = Blueprint('login', __name__)

# login form
class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField('Password', validators=[DataRequired()]) 
    stay_logged_in = BooleanField('Remember me')
    submit = SubmitField('Login')
    
# login route
@login.route('/login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Form data:", form.data)
        user = Users.query.filter_by(login=form.login.data).first()
        if user:
            print("User found:", user.login)
        else:
            print("User not found")

        if user and user.check_password(form.password.data):
            print("Password is correct")
            login_user(user, remember=form.stay_logged_in.data)
            flash('Login successful!')
            next_page = request.args.get('next') 
            return redirect(next_page or url_for('main.home'))  
        else:
            print("Invalid credentials")
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for('login.user_login'))  
    else:
        print("Form validation failed")
        print("Form errors:", form.errors)
    return render_template("auth/signin.html", form=form)

# Logout route
@login.route('/logout')
@login_required
def user_logout():
    logout_user()
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# Setting user login
@login.before_request
def before_request():
    g.user = current_user if current_user.is_authenticated else None
    
@login.route('/profile')
@login_required
def user_profile():
    return render_template('user.html')