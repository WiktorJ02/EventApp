from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.users import Users
from app import db

admin = Blueprint('admin', __name__)

# User list route
@admin.route('/user-list')
@login_required
def user_list():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('main.home'))
    
    users = Users.query.all()
    return render_template('user_list.html', users=users)

# Block users route
@admin.route('/block-user/<int:user_id>')
@login_required
def block_user(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'error')
        return redirect(url_for('main.home'))
    
    user = Users.query.get(user_id)
    if user:
        if user.is_admin:
            flash('You cannot block or unblock an admin user.', 'error')
        else:
            user.is_blocked = not user.is_blocked
            db.session.commit()
            action = 'unblocked' if not user.is_blocked else 'blocked'
            flash(f'User {user.login} has been {action}.', 'success')
    else:
        flash('User not found.', 'error')
    
    return redirect(url_for('admin.user_list'))