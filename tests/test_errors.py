# tests/test_errors.py

import unittest

from tests.base import BaseTestCase


class TestErrorHandling(BaseTestCase):
    """Test application error handling."""

    def test_404_error(self):
        """Test 404 not found error handling."""
        response = self.client.get('/21309gj0')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'<h1>404 - File Not Found</h1>', response.data)

    def test_500_error(self):
        """Test 500 internal server error handling."""
        response = self.client.get('/testing/500')
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'<h1>500 - Internal Server Error</h1>', response.data)


if __name__ == '__main__':
    unittest.main()
