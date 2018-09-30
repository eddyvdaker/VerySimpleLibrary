# manage.py

import unittest
from flask.cli import FlaskGroup

from app import create_app, db
from app.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    """Recreates the database"""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    """Seeds the database"""
    admin = User(username='admin', admin=True)
    admin.set_password('superstrongpassword')
    db.session.add(admin)

    user = User(username='user', admin=False)
    user.set_password('superstrongpassword')
    db.session.add(user)
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()
