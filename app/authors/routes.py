# app/authors/routes.py

from flask import render_template, abort
from flask_login import login_required

from app.authors import bp
from app.models import Author


@bp.route('/authors')
@login_required
def overview():
    authors = Author.query.order_by(Author.name).all()
    return render_template('authors/overview.html', title='Author Overview',
                           authors=authors)


@bp.route('/authors/<int:id>')
@login_required
def details(id):
    author = Author.query.filter_by(id=id).first()
    if not author:
        abort(404)
    return render_template('authors/details.html', author=author,
                           title=f'Author: {author.name}')
