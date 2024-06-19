from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.publications import Publications

profile = Blueprint('profile', __name__)

@profile.route('/myprofile')
@login_required
def view_profile():
    user = current_user
    publications = Publications.query.filter_by(creating_user_id=user.id).all()
    return render_template('my_profile.html', publications=publications, user=user)