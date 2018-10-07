# tests/test_model_author.py

import unittest

from app.models import Author
from tests.base import BaseTestCase, db


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

    def test_author_book_count(self):
        """Tests if the author book count method works correctly."""
        author = self.add_author('author1')
        book = self.add_book()
        self.assertEqual(author.number_of_books_written(), 0)
        author.books.append(book)
        db.session.commit()
        self.assertEqual(author.number_of_books_written(), 1)


if __name__ == '__main__':
    unittest.main()
