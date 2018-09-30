# tests/base.py

from flask_testing import TestCase

from app import create_app, db
from app.models import User


app = create_app(app_settings='app.config.TestingConfig')


def add_user(username='test', password='somepassword'):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


class BaseTestCase(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username='test', password='somepassword'):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)
