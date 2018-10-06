# app/books/forms.py

from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


class DeleteConfirmation(FlaskForm):
    confirmation = BooleanField('Are you sure you want to delete the book? '
                                '(this cannot be undone)')
    submit = SubmitField()
