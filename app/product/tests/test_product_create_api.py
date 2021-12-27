from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.utils_test import sample_user, sample_super_group, \
    sample_category

PRODUCT_CREATE_URL = reverse('product:product-create')


class PublicProductCreateApiTest(TestCase):
    """Public test suits for Product Create API"""

    def setUp(self):
        self.superuser = sample_user()
        sample_super_group(user=self.superuser)
        self.no_permission_user = sample_user(email="NoPermission@test.com")
        self.category = sample_category(user=self.superuser)
        self.client = APIClient()

    def test_product_create_401(self):
        """Test create product got 401(Unauthenticated)"""
        payload = {
            'name': '401',
            'category': self.category.id
        }
        res = self.client.post(path=PRODUCT_CREATE_URL, data=payload,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductCreateApiTest(PublicProductCreateApiTest):
    """Private test suits for Product Create API"""

    def setUp(self):
        super().setUp()

    def test_product_create_201(self):
        """Test create product got 201(Successful)"""
        self.client.force_authenticate(self.superuser)
        payload = {
            'name': '201',
            'category': self.category.id
        }
        res = self.client.post(path=PRODUCT_CREATE_URL, data=payload,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['created_by'], self.superuser.id)

    def test_product_create_403(self):
        """Test create product got 403(No Permission)"""
        self.client.force_authenticate(self.no_permission_user)
        payload = {
            'name': '403',
            'category': self.category.id
        }
        res = self.client.post(path=PRODUCT_CREATE_URL, data=payload,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_create_invalid_payload_400(self):
        """Test create product with invalid payload got 400(Bad Request)"""
        self.client.force_authenticate(self.superuser)
        payload = {
            'name': {'400': 'Dictionary instead of String'},
            'category': self.category.id
        }
        res = self.client.post(path=PRODUCT_CREATE_URL, data=payload,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_create_missing_mandatory_400(self):
        """Test create product missing mandatory got 400(Bad Request)"""
        self.client.force_authenticate(self.superuser)
        payload = {}
        res = self.client.post(path=PRODUCT_CREATE_URL, data=payload,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
