# tests/test_users.py

import unittest

from app.models import User
from tests.base import BaseTestCase, add_user


class TestProfile(BaseTestCase):
    """Test the users blueprint."""

    def test_profile_page(self):
        """Test if the users page is available."""
        add_user()
        self.login()
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Profile', response.data)
        self.assertIn(b'<b>Username:</b> test', response.data)
        self.assertIn(b'/change_password">Change Password</a>', response.data)

    def test_profile_page_logged_out(self):
        """Test if profile page redirects to login page if not logged in."""
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'<a href="/login?next=%2Fprofile">/login?next=%'
                      b'2Fprofile</a>', response.data)

    def test_change_password_page(self):
        """Tests if the change password page is available."""
        add_user()
        self.login()
        response = self.client.get('/change_password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Change Password</h1>', response.data)

    def test_change_password(self):
        """Tests if changing the password through the profile page works."""
        add_user()
        self.login()
        response = self.client.post(
            '/change_password',
            data=dict({
                'old_password': 'somepassword',
                'new_password': 'someotherpassword',
                'new_password_2': 'someotherpassword',
                'submit': 'Change Password'
            }),
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'<a href="/change_password">', response.data)
        user = User.query.filter_by(username='test').first()
        self.assertTrue(user.check_password('someotherpassword'))


if __name__ == '__main__':
    unittest.main()
