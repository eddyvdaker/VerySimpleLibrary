# tests/test_bp_main.py

import unittest

from tests.base import BaseTestCase


class TestMain(BaseTestCase):
    """Tests for the main blueprint."""

    def test_homepage(self):
        """Test if the homepage is available."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<p>Welcome to the VerySimpleLibrary', response.data)


if __name__ == '__main__':
    unittest.main()
