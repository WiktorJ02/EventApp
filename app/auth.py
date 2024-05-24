from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from app import authentication as at




class RegistrationForm(FlaskForm):
    first_name = StringField('Name:')
    last_name = StringField("Last name")
    birth_date = DateField('Birth date', format='%Y-%m-%d', validators=[validators.DataRequired()])
    

@at.route('/register')
def register_user():
    form = RegistrationForm()
    return render_template('auth/registration.html', form = form)