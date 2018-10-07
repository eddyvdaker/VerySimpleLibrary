# app/books/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import BooleanField, SubmitField, StringField, TextAreaField, \
    SelectField, DateField
from wtforms.validators import DataRequired


class DeleteConfirmation(FlaskForm):
    confirmation = BooleanField('Are you sure you want to delete the book? '
                                '(this cannot be undone)')
    submit = SubmitField('Delete')


class UploadBookForm(FlaskForm):
    file = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Upload')


class BookMetaDataForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    language = SelectField('Language', validators=[DataRequired()])
    file_type = SelectField('File Type', validators=[DataRequired()])
    publish_date = DateField('Publish Date')
    submit = SubmitField('Submit')
