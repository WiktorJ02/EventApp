from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.publications import Publications
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app import db
from app.models.ratings import Ratings

profile = Blueprint('profile', __name__)
# Forms
class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Change Email')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=60)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

# Routes
@profile.route('/myprofile')
@login_required
def view_profile():
    user = current_user
    publications = Publications.query.filter_by(creating_user_id=user.id).order_by(Publications.creation_date.desc()).all()
    change_email_form = ChangeEmailForm()
    change_password_form = ChangePasswordForm()
    for pub in publications:
        avg_rating = db.session.query(db.func.avg(Ratings.rating)).filter(Ratings.publication_id == pub.id).scalar()
        pub.average_rating = round(avg_rating, 1) if avg_rating else 0
    return render_template('my_profile.html', publications=publications, user=user, change_email_form=change_email_form, change_password_form=change_password_form)

@profile.route('/change_email', methods=['POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Your email has been updated.', 'success')
        return redirect(url_for('profile.view_profile'))
    return redirect(url_for('profile.view_profile'))

@profile.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'error')
            return redirect(url_for('profile.view_profile'))
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('profile.view_profile'))
    flash('Failed to change password. Please try again.', 'error')
    return redirect(url_for('profile.view_profile'))