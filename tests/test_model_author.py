# tests/test_model_author.py

import unittest

from app.models import Author
from tests.base import BaseTestCase


class TestModelAuthor(BaseTestCase):
    """Tests the behaviour of the author model."""

    def test_create_author(self):
        """Tests if creating a new author is possible."""
        author = Author(name='Some Author')
        self.add_to_db(author)

    def test_add_book_to_author(self):
        """Tests if it is possible to add a book to an author."""
        author = Author(name='Some Author')
        book = self.add_book()
        author.books.append(book)
        self.add_to_db(author)

        author = Author.query.all()[0]
        self.assertEqual(author.books[0], book)


if __name__ == '__main__':
    unittest.main()
