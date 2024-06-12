from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.users import Users

admin = Blueprint('admin', __name__)

@admin.route('/user-list')
@login_required
def user_list():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('main.home'))
    
    users = Users.query.all()
    return render_template('user_list.html', users=users)
