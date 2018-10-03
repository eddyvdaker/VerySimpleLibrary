# tests/test_model_user.py

import unittest

from app import db
from tests.base import BaseTestCase
from app.models import User


class TestUserModel(BaseTestCase):
    """Test the User model behavior."""

    def test_user_adding(self):
        """Tests if adding a user works correctly."""
        user = User(username='test')
        user.set_password('somepassword')
        db.session.add(user)
        db.session.commit()
        self.assertIn(user, User.query.all())

    def test_user_repr(self):
        """Tests if the user representation is correct."""
        user = self.add_user()
        self.assertEqual(str(user), '<User test>')

    def test_user_password(self):
        """Tests if password for a user works correctly."""
        user = self.add_user(password='password1234')
        self.assertTrue(user.check_password('password1234'))

    def test_user_admin_setting(self):
        """Tests if the admin setting is defaulted to false."""
        user = self.add_user()
        self.assertFalse(user.admin)

    def test_user_set_admin_to_true(self):
        """Tests setting admin to true."""
        user = self.add_user()
        user.admin = True
        db.session.commit()
        self.assertTrue(user.admin)


if __name__ == '__main__':
    unittest.main()
