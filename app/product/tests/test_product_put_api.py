from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.sample_test import sample_user, sample_super_group, \
    sample_category, sample_product


class PublicProductPutApiTest(TestCase):
    """Public test suits for Product Put API"""

    @staticmethod
    def get_url(product_id):
        return reverse('product:product-put', args=[product_id])

    def setUp(self):
        self.superuser = sample_user()
        sample_super_group(user=self.superuser)
        self.no_permission_user = sample_user(email="NoPermssion@test.com")
        self.category = sample_category(user=self.superuser)
        self.product = sample_product(user=self.superuser,
                                      category=self.category)
        self.client = APIClient()

    def test_put_product_401(self):
        """Test put product API got 401(Unauthenticated)"""
        url = self.get_url(self.product.id)
        res = self.client.put(url, data={}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductPutApiTest(PublicProductPutApiTest):
    """Private test suits for Product Put API"""

    def test_put_product_200(self):
        """Test put product got 200(Successful)"""
        self.client.force_authenticate(user=self.superuser)
        payload = {
            'name': '200',
            'category': self.category.id
        }
        url = self.get_url(self.product.id)
        res = self.client.put(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['updated_by'], self.superuser.id)

    def test_put_product_403(self):
        """Test put product got 403(No Permissions)"""
        self.client.force_authenticate(user=self.no_permission_user)
        payload = {
            'name': '403',
            'category': self.category.id
        }
        url = self.get_url(self.product.id)
        res = self.client.put(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_product_invalid_payload_400(self):
        """Test put product got 400(Invalid payload)"""
        self.client.force_authenticate(user=self.superuser)
        payload = {
            'name': {'400': 'Dictionary instead of String'},
            'category': self.category.id
        }
        url = self.get_url(self.product.id)
        res = self.client.put(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_product_missing_mandatory_400(self):
        """Test put product got 400(missing mandatory"""
        self.client.force_authenticate(user=self.superuser)
        payload = {
            'name': '400',
            'description': 'Missing category in payload'
        }
        url = self.get_url(self.product.id)
        res = self.client.put(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_product_404(self):
        """Test put product got 400(missing mandatory"""
        self.client.force_authenticate(user=self.superuser)
        payload = {
            'name': '404',
            'description': 'Missing category in payload'
        }
        url = self.get_url(123411234)
        res = self.client.put(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
