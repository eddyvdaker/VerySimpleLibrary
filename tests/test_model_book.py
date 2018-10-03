# tests/test_model_book.py

import unittest

from datetime import date

from app.models import Book
from tests.base import BaseTestCase


class TestModelBook(BaseTestCase):
    """Tests the behaviour of the book model."""

    def test_create_book(self):
        """Tests if a new book entry can be created."""
        file = '/tmp/some-test-book.pdf'
        book = Book(title='book', publish_date=date.today(), file=file,
                    file_type='pdf')
        self.add_to_db(book)


if __name__ == '__main__':
    unittest.main()
