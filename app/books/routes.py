# app/books/routes.py

from flask import render_template, abort
from flask_login import login_required

from app.books import bp
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
