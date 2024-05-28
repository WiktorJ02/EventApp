from flask import render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app import authentication as at, db
from app.models.users import Users
from flask_bcrypt import Bcrypt
from datetime import datetime
import pytz
import traceback

bcrypt = Bcrypt()

# registration form
class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('Repeat password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=32)])
    first_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=32)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=32)])
    birth_date = DateField('Birth date', format='%Y-%m-%d', validators=[DataRequired()])
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
            confirm = form.confirm.data,
            password = hashed_password,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            birth_date = form.birth_date.data,
        )
            db.session.add(new_user)
            db.session.commit()
            flash('Form successfully submitted')
            return 'Form successfully submitted'
        except Exception as e:
            db.session.rollback()
            print(f'error {e}')
            print(traceback.format_exc())
            flash('Error!!!!')
    else:
        print(form.errors)
    return render_template('auth/registration.html', form=form)