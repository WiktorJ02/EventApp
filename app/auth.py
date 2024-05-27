from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from app import authentication as at




class RegistrationForm(FlaskForm):
    login = StringField('Login: ')
    first_name = StringField('Name:')
    last_name = StringField("Last name")
    birth_date = DateField('Birth date', format='%Y-%m-%d', validators=[validators.DataRequired()])
    submit = SubmitField('Register')
    

@at.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process form data (e.g., save to database)
        return 'Form successfully submitted'
    else:
        print(form.errors)  # Print form errors to console for debugging
    return render_template('auth/registration.html', form=form)