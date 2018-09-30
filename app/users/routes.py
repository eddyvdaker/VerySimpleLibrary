# app/users/routes.py

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.users import bp
from app.users.forms import ChangePasswordForm


@bp.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', title='Profile')


@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        password = form.new_password.data
        if not current_user.check_password(old_password):
            flash('wrong password')
            return redirect(url_for('users.change_password'))
        current_user.set_password(password)
        db.session.commit()
        flash('Password changed')
        return redirect(url_for('users.change_password'))
    return render_template('users/change_password.html', form=form,
                           title='Change Password')
