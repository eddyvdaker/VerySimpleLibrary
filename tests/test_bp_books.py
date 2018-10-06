# tests/test_bp_books.py

import unittest

from app.models import Book
from tests.base import BaseTestCase


class TestBooks(BaseTestCase):
    """Tests the behaviour for the books blueprint."""

    def test_books_overview(self):
        """Tests the book overview page."""
        self.seed_test_db()
        self.login(username='user')
        response = self.client.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Books Overview</h1>', response.data)
        self.assertIn(b'book1', response.data)
        self.assertIn(b'book2', response.data)
        self.assertIn(b'<a href="/books/1">book1', response.data)

    def test_books_overview_admin_delete_button(self):
        """Tests if the admin shows a delete button for each book."""
        self.seed_test_db()
        self.login(username='admin')
        response = self.client.get('/books')
        self.assertIn(b'Delete', response.data)

    def test_books_overview_non_admin_delete_button(self):
        """Tests if a non-admin user shows a delete button."""
        self.seed_test_db()
        self.login(username='user')
        response = self.client.get('/books')
        self.assertNotIn(b'Delete', response.data)

    def test_books_delete_link(self):
        """Tests if the delete book links works."""
        self.seed_test_db()
        self.login(username='admin')

    def test_book_details_page(self):
        """Tests if the book details page is available."""
        self.seed_test_db()
        self.login(username='user')
        response = self.client.get('/books/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'book1', response.data)
        self.assertNotIn(b'book2', response.data)

    def test_book_delete(self):
        """Tests if the book delete page works correctly."""
        self.seed_test_db()
        self.login(username='admin')
        response = self.client.post(
            '/books/1/delete',
            data=dict({
                'confirmation': True
            }),
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'<a href="/books', response.data)
        self.assertNotIn('book1', [x.title for x in Book.query.all()])


if __name__ == '__main__':
    unittest.main()
