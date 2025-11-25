from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class UserModelTests(TestCase):
    """Test the custom User model."""

    def test_auth_user_model_setting(self):
        """Verify AUTH_USER_MODEL is set correctly."""
        self.assertEqual(settings.AUTH_USER_MODEL, 'accounts.User')

    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser."""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )

        self.assertEqual(admin.username, 'admin')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_user_str_with_email(self):
        """Test __str__ returns email when available."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.assertEqual(str(user), 'test@example.com')

    def test_user_str_without_email(self):
        """Test __str__ returns username when email is empty."""
        user = User.objects.create_user(
            username='nomail',
            password='testpass123'
        )

        self.assertEqual(str(user), 'nomail')

    def test_user_model_is_custom(self):
        """Verify we're using the custom User model, not Django's default."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.assertEqual(user.__class__.__name__, 'User')
        self.assertEqual(user.__class__.__module__, 'accounts.models')

    def test_db_table_name(self):
        """Verify custom db_table is set correctly."""
        self.assertEqual(User._meta.db_table, 'auth_user')

    def test_user_authentication(self):
        """Test user can authenticate with password."""
        user = User.objects.create_user(
            username='testuser',
            password='correctpass'
        )

        # Correct password
        self.assertTrue(user.check_password('correctpass'))

        # Wrong password
        self.assertFalse(user.check_password('wrongpass'))
