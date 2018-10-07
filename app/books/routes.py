# app/books/routes.py

import os

from datetime import datetime
from flask import render_template, abort, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from secrets import token_urlsafe
from shutil import copyfile

from app import db
from app.admin.decorator import admin_required
from app.books import bp
from app.books.forms import DeleteConfirmation, UploadBookForm, BookMetaDataForm
from app.books.metadata import get_meta_data
from app.models import Book, Language, Author


@bp.route('/books')
@login_required
def overview():
    books = Book.query.order_by(Book.title).all()
    return render_template('books/overview.html', title='Books Overview',
                           books=books)


@bp.route('/books/<int:id>')
@login_required
def details(id):
    book = Book.query.filter_by(id=id).first()
    if not book:
        abort(404)
    return render_template('books/details.html', title=f'Book: {book.title}',
                           book=book)


@bp.route('/books/<int:id>/delete', methods=['GET', 'POST'])
@admin_required
def delete_book(id):
    book = Book.query.filter_by(id=id).first()
    if not book:
        abort(404)
    form = DeleteConfirmation()
    if form.validate_on_submit():
        if form.confirmation.data:
            os.remove(book.file)
            for author in book.authors:
                book.authors.remove(author)
            db.session.commit()
            db.session.delete(book)
            db.session.commit()
            flash(f'{book.title} deleted')
            return redirect(url_for('books.overview'))
    return render_template('books/delete.html', title=f'Delete {book.title}',
                           form=form)


@bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_book(id):
    book = Book.query.filter_by(id=id).first()
    if not book:
        abort(404)
    form = BookMetaDataForm()

    form.language.choices = [(l.code, l.to_name(l.code)) for l in
                             Language.query.all()]
    form.file_type.choices = [(ft, ft) for ft in
                              current_app.config['FILE_TYPES']]

    if form.validate_on_submit():
        book.title = form.title.data

        for author in book.authors:
            book.authors.remove(author)

        author_names = form.authors.data.split(';')
        for author_name in author_names:
            author_name = author_name.strip()
            author = Author.query.filter_by(name=author_name).first()
            if not author:
                author = Author(name=author_name)
                db.session.add(author)
                db.session.commit()
            book.authors.append(author)

        lang = Language.query.filter_by(code=form.language.data).first()
        book.language = lang

        book.publish_date = form.publish_date.data

        book.file_type = form.file_type.data

        db.session.commit()
        flash('Book information updated')
        return redirect(url_for('books.details', id=book.id))
    else:
        form.title.data = book.title

        authors = ""
        for i, author in enumerate(book.authors):
            if i:
                authors += '; ' + author.name
            else:
                authors += author.name
        form.authors.data = authors

        form.language.data = book.language.code
        form.file_type.data = book.file_type

        form.publish_date.data = book.publish_date
    return render_template('books/edit_metadata.html', title='Edit Metadata',
                           form=form)


@bp.route('/books/upload', methods=['GET', 'POST'])
@login_required
def upload_book():
    form = UploadBookForm()
    if form.validate_on_submit():
        filename = token_urlsafe(10)
        path = os.path.join(current_app.config['TMP_FOLDER'], filename)
        form.file.data.save(path)
        return redirect(url_for('books.edit_upload_metadata', file=filename))
    return render_template('books/upload.html', form=form, title='Upload Book')


@bp.route('/books/upload/<file>', methods=['GET', 'POST'])
@login_required
def edit_upload_metadata(file):
    form = BookMetaDataForm()
    tmp_path = os.path.join(current_app.config['TMP_FOLDER'], file)

    form.language.choices = [(l.code, l.to_name(l.code)) for l in
                             Language.query.all()]
    form.file_type.choices = [(ft, ft) for ft in
                              current_app.config['FILE_TYPES']]

    if form.validate_on_submit():
        filename = (form.title.data + '.' + form.file_type.data).\
            replace(' ', '_')
        new_path = os.path.join(current_app.config['FILE_FOLDER'], filename)

        if not os.path.exists(current_app.config['FILE_FOLDER']):
            os.mkdir(current_app.config['FILE_FOLDER'])

        copyfile(tmp_path, new_path)
        os.remove(tmp_path)

        book = Book(title=form.title.data, file_type=form.file_type.data,
                    file=new_path)

        if form.publish_date.data:
            book.publish_date = form.publish_date.data
        lang = Language.query.filter_by(code=form.language.data).first()
        if lang:
            book.language = lang
        book.set_hash()
        book.uploader = current_user

        author_names = form.authors.data.split(';')
        for author_name in author_names:
            author_name = author_name.strip()
            author = Author.query.filter_by(name=author_name).first()
            if not author:
                author = Author(name=author_name)
                db.session.add(author)
                db.session.commit()
            book.authors.append(author)
        db.session.add(book)
        db.session.commit()
        flash(f'Uploaded {book.title}')
        return redirect(url_for('books.details', id=book.id))
    else:
        metadata = get_meta_data(tmp_path)
        form.title.data = metadata['title']
        form.authors.data = metadata['authors']
        form.language.data = metadata['language']
        form.file_type.data = metadata['file_type']
        form.publish_date.data = datetime.strptime(metadata['publish_date'],
                                                   '%Y-%m-%d')
    return render_template('books/edit_metadata.html', form=form,
                           title='Edit Meta Data')
