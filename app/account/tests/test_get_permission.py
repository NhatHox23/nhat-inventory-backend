from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.utils.utils_test import sample_user

PERMISSION_URL = reverse("account:list-permission")


class PublicPermissionApiTest(TestCase):
    """Test Permissions API without log-in"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()

    def test_list_permission_fail_no_authentication(self):
        """Test that listing permission fail unauthenticated"""
        res = self.client.get(PERMISSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePermissionApiTest(TestCase):
    """Test Permission API with log-in"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_list_permission_successfully(self):
        """Test that list permission successfully"""
        res = self.client.get(PERMISSION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
