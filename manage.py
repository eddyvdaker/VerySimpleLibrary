# manage.py

import coverage
import unittest

from datetime import date
from flask.cli import FlaskGroup

from app import create_app, db
from app.models import User, Author, Language, Book

app = create_app()
cli = FlaskGroup(create_app=create_app)

COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        '*.db',
        'templates/*'
    ]
)
COV.start()

# Helper functions


def add_user(username, password, admin=False):
    user = User(username=username, admin=admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def add_language(code):
    lang = Language(code=code)
    db.session.add(lang)
    db.session.commit()
    return lang


def add_author(name, books=None):
    author = Author(name=name)
    if books:
        for book in books:
            author.books.append(book)
    db.session.add(author)
    db.session.commit()
    return author


def add_book(title, publish_date=date.today(), create_file=False, uploader=None,
             authors=None, language=None):
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


# CLI commands


@cli.command()
def recreate_db():
    """Recreates the database"""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    """Seeds the database"""
    add_user('admin', 'superstrongpassword', admin=True)


@cli.command()
def seed_dev_db():
    """Seeds the database for development"""
    admin = add_user('admin', 'superstrongpassword', admin=True)
    user = add_user('user', 'otherstrongpassword')

    author1 = add_author('author1')
    author2 = add_author('author2')

    nl = add_language('NL')
    us = add_language('US')

    add_book('book1', create_file=True, uploader=admin, authors=[author1],
             language=nl)
    add_book('book2', create_file=True, uploader=admin,
                     authors=[author1, author2], language=us)
    add_book('book3', create_file=True, uploader=user, authors=[author2],
             language=us)


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()
