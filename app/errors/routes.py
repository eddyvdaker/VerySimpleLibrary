# app/errors/routes.py

from flask import abort, current_app

from app.errors import bp


@bp.route('/testing/500')
def test_500_error():
    """Testing route for testing 500 error handling. Only active in while
    running automated tests.
    """
    if current_app.config['TESTING']:
        abort(500)
    abort(404)
