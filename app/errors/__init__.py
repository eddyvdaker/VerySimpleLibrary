# app/errors/__init__.py

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers, routes
