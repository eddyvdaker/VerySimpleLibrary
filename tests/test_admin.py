# tests/test_admin.py

from tests.base import BaseTestCase, add_user
from app.models import User


class TestAdminPanel(BaseTestCase):
    """Test the admin panel."""

    def test_admin_panel(self):
        """Tests if the admin panel is available for an admin."""
        add_user(admin=True)
        self.login()

        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Admin Panel</h1>', response.data)

    def test_admin_user_overview(self):
        """Tests if the user overview is available."""
        add_user(admin=True)
        self.login()

        response = self.client.get('/admin/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Admin Panel: Users</h1>', response.data)
        self.assertIn(b'<td>1</td>', response.data)
        self.assertIn(b'<td>test</td>', response.data)

    def test_admin_adding_user(self):
        """Tests adding new users."""
        add_user(admin=True)
        self.login()

        self.assertEqual(len(User.query.all()), 1)
        response = self.client.post(
            '/admin/users/add',
            data=dict({
                'username': 'someusername',
                'password': 'somepassword',
                'password_2': 'somepassword'
            }),
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'<a href="/admin/users">', response.data)
        self.assertEqual(len(User.query.all()), 2)
