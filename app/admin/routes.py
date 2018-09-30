# app/admin/routes.py

from flask import render_template

from app.admin import bp
from app.admin.decorator import admin_required
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
