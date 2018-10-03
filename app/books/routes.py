# app/books/routes.py

from flask import render_template
from flask_login import login_required

from app.books import bp
from app.models import Book


@bp.route('/books')
@login_required
def overview():
    books = Book.query.all()
    return render_template('books/overview.html', title='Books Overview',
                           books=books)
