# tests/test_bp_authors.py

import unittest

from tests.base import BaseTestCase


class TestAuthors(BaseTestCase):
    """Tests the behaviour for the authors blueprint."""

    def test_author_overview(self):
        """Tests the author overview page."""
        self.seed_test_db()
        self.login(username='user')
        response = self.client.get('/authors')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Author Overview', response.data)
        self.assertIn(b'author1', response.data)
        self.assertIn(b'author2', response.data)

    def test_author_details(self):
        """Tests the author details page."""
        self.seed_test_db()
        self.login(username='user')
        response = self.client.get('/authors/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Author: author1', response.data)
        self.assertIn(b'book1', response.data)
        self.assertIn(b'book2', response.data)
        self.assertNotIn(b'book3', response.data)


if __name__ == '__main__':
    unittest.main()
