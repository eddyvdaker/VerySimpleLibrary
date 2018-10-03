# tests/test_model_language.py

import unittest

from app.models import Language
from tests.base import BaseTestCase


class TestModelLanguage(BaseTestCase):
    """Test the behaviour of the language model."""

    def test_create_language(self):
        """Tests the creation of a new language entry."""
        self.assertEqual(len(Language.query.all()), 0)
        lang = Language(code='EN')
        self.add_to_db(lang)


if __name__ == '__main__':
    unittest.main()
