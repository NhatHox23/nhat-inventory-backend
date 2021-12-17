from django.test import TestCase
from django.contrib.auth import get_user_model


class UserActionTest(TestCase):
    def test_create_user(self):
        """Test that create user successful"""
        user = get_user_model().objects.create_user(
            "test_create@nhat.com",
            "123456789"
        )
        self.assertEqual(str(user), "test_create@nhat.com")
        self.assertTrue(user.check_password("123456789"))
        self.assertEqual(user.is_staff, False)

    def test_create_user_no_email(self):
        """Test that create user with no email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="123456789"
            )

    def test_create_superuser(self):
        """Test that create superuser successful"""
        superuser = get_user_model().objects.create_superuser(
            "test_create_super@nhat.com",
            "123456789"
        )
        self.assertEqual(str(superuser), "test_create_super@nhat.com")
        self.assertTrue(superuser.check_password("123456789"))
        self.assertEqual(superuser.is_staff, True)

    def test_create_superuser_no_email(self):
        """Test that create superuser with no email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="123456789"
            )
