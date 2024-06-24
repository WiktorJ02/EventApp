from flask import Blueprint, render_template, redirect, url_for, flash, request
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

    search_login = request.args.get('search_login', '')
    search_email = request.args.get('search_email', '')
    search_first_name = request.args.get('search_first_name', '')
    search_last_name = request.args.get('search_last_name', '')
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    query = Users.query

    if search_login:
        query = query.filter(Users.login.ilike(f"%{search_login}%"))
    if search_email:
        query = query.filter(Users.email.ilike(f"%{search_email}%"))
    if search_first_name:
        query = query.filter(Users.first_name.ilike(f"%{search_first_name}%"))
    if search_last_name:
        query = query.filter(Users.last_name.ilike(f"%{search_last_name}%"))

    if sort_order == 'asc':
        query = query.order_by(getattr(Users, sort_by).asc())
    else:
        query = query.order_by(getattr(Users, sort_by).desc())

    users = query.all()

    return render_template('user_list.html', users=users, search_login=search_login, search_email=search_email, search_first_name=search_first_name, search_last_name=search_last_name, sort_by=sort_by, sort_order=sort_order)

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
