from flask import Blueprint

bp = Blueprint('main', __name__)


@bp.route('/users')
def index():
    return 'hi'
