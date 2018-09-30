# app/errors/handlers.py

from flask import render_template

from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error.html', title='404 - File Not Found'), 404


@bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error.html',
                           title='500 - Internal Server Error'), 500
