# app/errors/routes.py

from flask import abort, current_app

from app.errors import bp


@bp.route('/testing/500')
def test_500_error():
    print(current_app.config['TESTING'])
    if current_app.config['TESTING']:
        abort(500)
    abort(404)
