from flask import render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app import authentication as at, db 
from app.models.users import Users
from flask_bcrypt import Bcrypt
import traceback
from datetime import datetime
import re

bcrypt = Bcrypt()

# validations for register form    
def login_exists(form, field):
    login_validation = Users.query.filter_by(login=field.data).first()
    if login_validation:
        raise ValidationError('Login already exists')

def email_exists(form, field):
    email_validation = Users.query.filter_by(email=field.data).first()
    if email_validation:
        raise ValidationError('Email already exists') 
    
def birth_date_validation(form, field):
    birth_date = field.data
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError('You must be at least 18 years old to register.')
    
def password_strength(form, field):
    password = field.data
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one number.')

# registration form
class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=32), login_exists])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=60), EqualTo('confirm', message = 'Passwords must match'), password_strength])
    confirm = PasswordField('Repeat password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=32), email_exists])
    first_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=32)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=32)])
    birth_date = DateField('Birth date', format='%Y-%m-%d', validators=[DataRequired(), birth_date_validation])
    submit = SubmitField('Register')

# registration route
@at.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        try: 
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = Users(
            login = form.login.data,
            password = hashed_password,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            birth_date = form.birth_date.data,
        )
            db.session.add(new_user)
            db.session.commit()
            return render_template('auth/congrats.html')
        except Exception as e:
            db.session.rollback()
            print(f'error {e}')
            print(traceback.format_exc())
            flash('Something went worng :(')
    else:
        print(form.errors)
    return render_template('auth/registration.html', form=form)