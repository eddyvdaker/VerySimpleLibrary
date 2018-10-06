# app/books/routes.py

from flask import render_template, abort, flash, redirect, url_for
from flask_login import login_required

from app import db
from app.admin.decorator import admin_required
from app.books import bp
from app.books.forms import DeleteConfirmation
from app.models import Book


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
            for author in book.authors:
                book.authors.remove(author)
            db.session.commit()
            db.session.delete(book)
            db.session.commit()
            flash(f'{book.title} deleted')
            return redirect(url_for('books.overview'))
    return render_template('books/delete.html', title=f'Delete {book.title}',
                           form=form)
