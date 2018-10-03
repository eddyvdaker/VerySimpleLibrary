# tests/test_model_book.py

import unittest

from datetime import date

from app.models import Book
from tests.base import BaseTestCase


class TestModelBook(BaseTestCase):
    """Tests the behaviour of the book model."""

    def test_create_book(self):
        """Tests if a new book entry can be created."""
        self.assertEqual(len(Book.query.all()), 0)
        file = '/tmp/some-test-book.pdf'
        book = Book(title='book', publish_date=date.today(), file=file,
                    file_type='pdf')
        self.add_to_db(book)
        self.assertEqual(len(Book.query.all()), 1)
        self.assertTrue(book.upload_date)


if __name__ == '__main__':
    unittest.main()
