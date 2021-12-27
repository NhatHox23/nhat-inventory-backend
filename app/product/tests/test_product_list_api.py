from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.sample_test import sample_user, sample_super_group, \
    sample_category, sample_product

PRODUCT_LIST_URL = reverse('product:product-list')


class PublicProductListApiTest(TestCase):
    """Public test suits for Product List API"""

    def setUp(self):
        self.superuser = sample_user()
        sample_super_group(user=self.superuser)
        self.category = sample_category(user=self.superuser)
        self.product = sample_product(user=self.superuser,
                                      category=self.category)
        self.client = APIClient()

    def test_list_product_401(self):
        """Test list product got 401(UnAuthenticated)"""
        res = self.client.get(path=PRODUCT_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductListApiTest(TestCase):
    """Private test suits for Product List API"""

    def setUp(self):
        self.superuser = sample_user()
        self.no_permission_user = sample_user(email="NoPermission@tesst.com")
        sample_super_group(user=self.superuser)
        self.category = sample_category(user=self.superuser)
        self.product = sample_product(user=self.superuser,
                                      category=self.category)
        self.client = APIClient()

    def test_list_product_200(self):
        """Test list product got 200(Successful)"""
        self.client.force_authenticate(user=self.superuser)
        res = self.client.get(PRODUCT_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)

    def test_list_product_403(self):
        """Test list product got 403(No Permissions)"""
        self.client.force_authenticate(user=self.no_permission_user)
        res = self.client.get(PRODUCT_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
