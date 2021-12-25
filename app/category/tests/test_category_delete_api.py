from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.utils_test import sample_user, sample_super_group, \
    sample_category


class PublicCategoryDeleteApiTest(TestCase):
    """Public test suits for Category Delete API"""

    @staticmethod
    def get_url(category_id):
        return reverse("category:category-delete", args=[category_id])

    def setUp(self):
        self.user = sample_user()
        sample_super_group(user=self.user)
        self.category = sample_category(user=self.user)
        self.client = APIClient()

    def test_category_delete_api_401(self):
        """Test that category deletes got 401(Unauthenticated)"""
        url = self.get_url(self.category.id)
        res = self.client.delete(path=url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryDeleteApiTest(TestCase):
    """Private test suits for Category Delete API"""

    @staticmethod
    def get_url(category_id):
        return reverse("category:category-delete", args=[category_id])

    def setUp(self):
        self.user = sample_user()
        self.user2 = sample_user(email="NoPermission@test.com")
        sample_super_group(user=self.user)
        self.category = sample_category(user=self.user)
        self.client = APIClient()

    def test_category_delete_api_204(self):
        """Test that category deletes api got 204(Not Found)"""
        self.client.force_authenticate(self.user)
        url = self.get_url(self.category.id)
        res = self.client.delete(path=url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_category_delete_api_403(self):
        """Test that category deletes api got 403(No Permissions)"""
        self.client.force_authenticate(self.user2)
        url = self.get_url(self.category.id)
        res = self.client.delete(path=url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_delete_api_404(self):
        """Test that category deletes api got 404(Not Found Category)"""
        self.client.force_authenticate(self.user)
        url = self.get_url(123123123)
        res = self.client.delete(path=url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
