from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.sample_test import sample_user, sample_super_group

CATEGORY_LIST_URL = reverse('category:category-list')


class PublicCategoryListApiTest(TestCase):
    """Public Test suits for Category List API"""

    def setUp(self):
        self.user = sample_user()
        sample_super_group(user=self.user)
        self.client = APIClient()

    def test_list_category_401(self):
        """Test that list category API return 401 (unauthenticated)"""
        res = self.client.get(CATEGORY_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryListApiTest(TestCase):
    """Private Test suits for Category List API"""

    def setUp(self):
        self.user = sample_user()
        self.user2 = sample_user(email="NoPermission@nhat.com")
        sample_super_group(user=self.user)
        self.client = APIClient()

    def test_list_category_200(self):
        """Test that list category API return 200 (Successful)"""
        self.client.force_authenticate(self.user)
        res = self.client.get(CATEGORY_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_category_403(self):
        """Test that list category API return 403 (No Permission)"""
        self.client.force_authenticate(self.user2)
        res = self.client.get(CATEGORY_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
