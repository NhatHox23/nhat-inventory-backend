from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.utils_test import sample_user, sample_super_group, \
    sample_product, sample_category


class PublicProductDeleteApiTest(TestCase):
    """Public test suits for Product Delete API"""

    @staticmethod
    def get_url(product_id):
        return reverse('product:product-delete', args=[product_id])

    def setUp(self):
        self.superuser = sample_user()
        sample_super_group(user=self.superuser)
        self.category = sample_category(user=self.superuser)
        self.product = sample_product(user=self.superuser,
                                      category=self.category)
        self.client = APIClient()

    def test_delete_product_401(self):
        """Test delete product got 401(Unauthenticated)"""
        url = self.get_url(self.product.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductDeleteApiTest(PublicProductDeleteApiTest):
    """Private test suits for Product Delete API"""

    def setUp(self):
        super().setUp()
        self.no_permission_user = sample_user(email='NoPermission@test.com')

    def test_delete_product_204(self):
        """Test delete product got 204(No Content)"""
        self.client.force_authenticate(user=self.superuser)
        url = self.get_url(self.product.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_403(self):
        """Test delete product got 403(No Permission)"""
        self.client.force_authenticate(user=self.no_permission_user)
        url = self.get_url(self.product.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_not_found_204(self):
        """Test delete product(not existed product) got 204(No Content)"""
        self.client.force_authenticate(user=self.superuser)
        url = self.get_url(100000)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
