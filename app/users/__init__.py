# app/users/__init__.py

from flask import Blueprint

bp = Blueprint('users', __name__)


import app.users.routes
