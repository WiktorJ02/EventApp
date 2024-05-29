from flask import render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from app import signin
from app.models.users import Users
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user

bcrypt = Bcrypt()

# login form
class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField('Password', validators=[DataRequired()]) 
    stay_logged_in = BooleanField('Remember me')
    submit = SubmitField('Login')
    
#login route
@signin.route('/login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid credentials. Please try again')
            
        login_user(user, form.stay_logged_in.data)
        return redirect(url_for('/'))
         
    return render_template("auth/signin.html", form=form)
