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


if __name__ == '__main__':
    unittest.main()
