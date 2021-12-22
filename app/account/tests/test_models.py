from django.test import TestCase
from django.contrib.auth import get_user_model


class AccountModelsTest(TestCase):
    def test_user_str(self):
        """Test that user return str representation as email"""
        user = get_user_model().objects.create_user(
            email="Test@nhat.com",
            password="123456"
        )
        self.assertEqual(str(user), 'Test@nhat.com')

