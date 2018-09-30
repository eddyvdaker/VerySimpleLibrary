# app/users/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password',
                                 validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password_2 = PasswordField('Retype New Password', validators=[
        DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')
