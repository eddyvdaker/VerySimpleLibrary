# app/admin/routes.py

from flask import render_template, flash, redirect, url_for

from app import db
from app.admin import bp
from app.admin.decorator import admin_required
from app.admin.forms import NewUserForm
from app.models import User


@bp.route('/admin')
@admin_required
def admin():
    return render_template('admin/admin-panel.html', title='Admin Panel')


@bp.route('/admin/users')
@admin_required
def users_overview():
    users = User.query.all()
    return render_template('admin/overview-users.html', users=users,
                           title='Admin Panel: Users')


@bp.route('/admin/users/add', methods=['GET', 'POST'])
@admin_required
def users_add():
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken')
            return redirect(url_for('admin.users_add'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash(f'User: {username} has been created')
        return redirect(url_for('admin.users_overview'))
    return render_template('admin/add_users.html', form=form,
                           title='Admin Panel: Add User')
