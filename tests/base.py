# tests/base.py

from datetime import date
from flask_testing import TestCase

from app import create_app, db
from app.models import User, Language, Author, Book


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

    def add_book(self, title='book', publish_date=date.today(),
                 create_file=False, uploader=None, authors=None, language=None):
        file = f'/tmp/{title}.pdf'
        book = Book(title=title, publish_date=publish_date, file=file,
                    file_type='pdf')
        if create_file:
            with open(file, 'w+') as file:
                file.write(title)
            book.set_hash()

        if uploader:
            book.uploader = uploader

        if language:
            book.language = language
        if authors:
            for author in authors:
                book.authors.append(author)

        db.session.add(book)
        db.session.commit()
        return book

    def seed_test_db(self):
        """Seed test db for more complex tests involving data from the
        database."""
        admin = self.add_user('admin', 'somepassword', admin=True)
        user = self.add_user('user', 'somepassword')

        author1 = self.add_author('author1')
        author2 = self.add_author('author2')

        nl = self.add_language('NL')
        us = self.add_language('US')

        self.add_book(title='book1', create_file=True, uploader=admin,
                      authors=[author1], language=nl)
        self.add_book('book2', create_file=True, uploader=admin,
                      authors=[author1, author2], language=us)
        self.add_book('book3', create_file=True, uploader=user,
                      authors=[author2], language=us)
