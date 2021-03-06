# tests/test_model_book.py

import os
import unittest

from datetime import date
from hashlib import sha256

from app.models import Book
from tests.base import BaseTestCase


class TestModelBook(BaseTestCase):
    """Tests the behaviour of the book model."""

    def test_create_book(self):
        """Tests if a new book entry can be created."""
        self.assertEqual(len(Book.query.all()), 0)
        file = '/tmp/some-test-book.pdf'
        file_hash = sha256(file.encode('utf-8')).hexdigest()
        book = Book(title='book', publish_date=date.today(), file=file,
                    file_type='pdf')
        self.add_to_db(book)
        self.assertEqual(len(Book.query.all()), 1)
        self.assertTrue(book.upload_date)

    def test_adding_language_to_book(self):
        """Tests setting a language for a book."""
        file = '/tmp/some-test-book.pdf'
        book = Book(title='book', publish_date=date.today(), file=file,
                    file_type='pdf')
        lang = self.add_language()
        book.language = lang
        self.add_to_db(book)

        book = Book.query.all()[0]

        self.assertEqual(book.language, lang)

    def test_setting_hash(self):
        """Tests calculating the hash for a file."""
        file = '/tmp/some-test-book.pdf'
        book = Book(title='book', publish_date=date.today(), file=file,
                    file_type='pdf')

        self.assertFalse(book.file_hash)
        if os.path.exists(file):
            os.remove(file)
        open(file, 'w+').close()
        book.set_hash()
        self.add_to_db(book)
        self.assertTrue(book.file_hash)

    def test_adding_uploader(self):
        """Tests if an uploader can be added to a book."""
        user = self.add_user()
        file = '/tmp/some-test-book.pdf'
        book = Book(title='book', publish_date=date.today(), file=file,
                    file_type='pdf')
        book.uploader = user
        self.add_to_db(book)

        book = Book.query.all()[0]
        self.assertEqual(book.uploader, user)

    def test_adding_author(self):
        """Tests if an author can be added to a book."""
        author = self.add_author()
        file = '/tmp/some-test-book.pdf'
        book = Book(title='book', publish_date=date.today(), file=file,
                    file_type='pdf')
        book.authors.append(author)
        self.add_to_db(book)

        book = Book.query.all()[0]
        self.assertEqual(book.authors[0], author)


if __name__ == '__main__':
    unittest.main()
