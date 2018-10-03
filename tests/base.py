# tests/base.py

from flask_testing import TestCase

from app import create_app, db
from app.models import User, Language, Author


app = create_app(app_settings='app.config.TestingConfig')


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    """Helper methods"""

    def add_to_db(self, to_add):
        db.session.add(to_add)
        db.session.commit()

    def login(self, username='test', password='somepassword'):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def add_user(self, username='test', password='somepassword', admin=False):
        user = User(username=username, admin=admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def add_language(self, code='US'):
        language = Language(code=code)
        db.session.add(language)
        db.session.commit()
        return language

    def add_author(self, name='some author'):
        author = Author(name=name)
        db.session.add(author)
        db.session.commit()
        return author
