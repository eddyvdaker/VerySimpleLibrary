# app/authors/__init_.py

from flask import Blueprint

bp = Blueprint('authors', __name__)

from app.authors import routes
