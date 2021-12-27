from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.sample_test import sample_user, sample_super_group, \
    sample_category


class PublicCategoryPatchApiTest(TestCase):
    """Public test suits for Category Patch API"""

    @staticmethod
    def get_url(category_id):
        return reverse('category:category-patch', args=[category_id])

    def setUp(self):
        self.user = sample_user()
        sample_super_group(user=self.user)
        self.category = sample_category(user=self.user)
        self.client = APIClient()

    def test_category_patch_401(self):
        """Test patch category got 401(unAuthenticated)"""
        payload = {
            "status": 2
        }
        url = self.get_url(self.category.id)
        res = self.client.patch(path=url, data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryPatchApiTest(TestCase):
    """Private test suits for Category Patch API"""

    @staticmethod
    def get_url(category_id):
        return reverse('category:category-patch', args=[category_id])

    def setUp(self):
        self.user = sample_user()
        self.user2 = sample_user(email="NoPermission@test.com")
        sample_super_group(user=self.user)
        self.category = sample_category(user=self.user)
        self.client = APIClient()

    def test_category_patch_200(self):
        """Test that category patch api got 200 (Successful)"""
        self.client.force_authenticate(self.user)
        payload = {
            "name": "Correct",
            "status": 2
        }
        url = self.get_url(self.category.id)
        res = self.client.patch(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['updated_by'], self.user.id)

    def test_category_patch_403(self):
        """Test that category patch api got 403 (No Permission)"""
        self.client.force_authenticate(self.user2)
        payload = {
            "name": "403",
            "status": 2
        }
        url = self.get_url(self.category.id)
        res = self.client.patch(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_patch_400_invalid_type_payload(self):
        """Test that category patch api got 400 (invalid type in payload)"""
        self.client.force_authenticate(self.user)
        payload = {
            "name": {"400": "Dictionary instead of String"}
        }
        url = self.get_url(self.category.id)
        res = self.client.patch(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_patch_200_partial_only_status_payload(self):
        """Test that category patch api got 200 (only status, test partial)"""
        self.client.force_authenticate(self.user)
        payload = {
            'status': 3
        }
        url = self.get_url(self.category.id)
        res = self.client.patch(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['updated_by'], self.user.id)

    def test_category_patch_404(self):
        """Test that category patch api got 404 (Not Found)"""
        self.client.force_authenticate(self.user)
        payload = {
            'status': 3
        }
        url = self.get_url(102321591823)
        res = self.client.patch(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
