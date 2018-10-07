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

    def test_code_to_country(self):
        """Tests if a code can be converted to language."""
        country = Language.to_name('US')
        self.assertEqual('United States', country)

    def test_non_existing_code_to_country(self):
        """Tests if a non existing code is handled correctly."""
        country = Language.to_name('AA')
        self.assertEqual('country code does not match a known country', country)

    def test_wrongly_formated_code_to_country(self):
        """Tests if a wrongly formated code is handled correctly."""
        country = Language.to_name('USAB')
        self.assertEqual('invalid country code', country)

    def test_country_to_code(self):
        """Tests if a country name can be converted to a code."""
        code = Language.to_code('United States')
        self.assertEqual('US', code)

        code = Language.to_code('United States', code_len=3)
        self.assertEqual('USA', code)

    def test_non_existing_country_to_code(self):
        """Tests if a non existing country is handled correctly."""
        code = Language.to_code('ABCDEFG')
        self.assertEqual('country not found', code)


if __name__ == '__main__':
    unittest.main()
