# tests/test_auth.py

import unittest

from tests.base import BaseTestCase, add_user


class TestLogin(BaseTestCase):
    """Tests for the login system of the auth blueprint."""

    def test_login_page(self):
        """Test if the login page exists."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Login', response.data)
        self.assertIn(b'<form', response.data)
        self.assertIn(b'name="username" required type="text"', response.data)
        self.assertIn(b'name="password" required type="password"',
                      response.data)
        self.assertIn(b'name="remember_me" type="checkbox"', response.data)
        self.assertIn(b'name="submit" type="submit"', response.data)

    def test_login_page_login(self):
        """Test if logging in through the login page works."""
        add_user()
        response = self.client.post(
            '/login',
            data=dict({
                'username': 'test',
                'password': 'somepassword'
            }),
            content_type='application/x-www-form-urlencoded',
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertIn(b'Welcome test,', response.data)

    def test_login_page_default_redirect(self):
        """Test if default redirect goes to homepage on successful login."""
        add_user()
        response = self.login()
        self.assertIn(b'Welcome test,', response.data)

    def test_login_link_shown(self):
        """Tests if the login link is shown for a anonymous user."""
        response = self.client.get('/')
        self.assertIn(b'>Login</a>', response.data)

    def test_login_link_not_shown(self):
        """Tests if the login link is not shown for logged in users."""
        add_user()
        self.login()
        response = self.client.get('/')
        self.assertNotIn(b'>Login</a>', response.data)


class TestLogout(BaseTestCase):
    """Tests the logout functionality."""

    def test_logout(self):
        """Test the logout link."""
        add_user()
        self.login()
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertNotIn(b'Welcome test,', response.data)

    def test_logout_link_shown(self):
        """Test if the logout link is shown if logged in."""
        add_user()
        self.login()
        response = self.client.get('/')
        self.assertIn(b'>Logout</a>', response.data)

    def test_logout_link_not_shown(self):
        """Check if the logout link is not shown for an anonymous user."""
        response = self.client.get('/')
        self.assertNotIn(b'>Logout</a>', response.data)


class TestAuthentication(BaseTestCase):
    """Tests whether the authentication works."""

    def test_login_required(self):
        """Test if login required works if logged in."""
        add_user()
        self.login()
        response = self.client.get('/testing/login_required')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

    def test_login_required_not_logged_in(self):
        """Test if login required works if not logged in."""
        response = self.client.get('/testing/login_required')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'<a href="/login?next=%2Ftesting%2Flogin_required">',
                         response.data)


if __name__ == '__main__':
    unittest.main()
