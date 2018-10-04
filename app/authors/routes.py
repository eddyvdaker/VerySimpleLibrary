# app/authors/routes.py

from flask import render_template
from flask_login import login_required

from app.authors import bp
from app.models import Author


@bp.route('/authors')
@login_required
def overview():
    authors = Author.query.order_by(Author.name).all()
    return render_template('authors/overview.html', title='Author Overview',
                           authors=authors)
