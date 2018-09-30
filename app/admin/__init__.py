# app/admin/__init__.py

from flask import Blueprint

bp = Blueprint('admin', __name__)

from app.admin import routes
