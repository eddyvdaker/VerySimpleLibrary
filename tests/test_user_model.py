# tests/test_user_model.py

import unittest

from app import db
from tests.base import BaseTestCase, add_user
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
        user = add_user()
        self.assertEqual(str(user), '<User test>')

    def test_user_password(self):
        """Tests if password for a user works correctly."""
        user = add_user(password='password1234')
        self.assertTrue(user.check_password('password1234'))


if __name__ == '__main__':
    unittest.main()
