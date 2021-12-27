from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.utils_test import sample_user, sample_super_group, \
    sample_category, sample_product


class PublicProductPatchApiTest(TestCase):
    """Public test suits for Product Patch API"""

    @staticmethod
    def get_url(product_id):
        return reverse('product:product-patch', args=[product_id])

    def setUp(self):
        self.superuser = sample_user()
        sample_super_group(user=self.superuser)
        self.category = sample_category(user=self.superuser)
        self.product = sample_product(user=self.superuser,
                                      category=self.category)
        self.client = APIClient()

    def test_patch_category_401(self):
        """Test patch category got 401(Unauthenticated)"""
        url = self.get_url(self.product.id)
        payload = {
            'name': '401'
        }
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductPatchAPiTest(PublicProductPatchApiTest):
    """Private test suits for Product Patch API"""

    def setUp(self):
        super().setUp()
        self.no_permission_user = sample_user(email="NoPermission@test.com")

    def test_patch_category_200(self):
        """Test patch category got 200(Successful)"""
        self.client.force_authenticate(self.superuser)
        url = self.get_url(self.product.id)
        payload = {
            'name': '200'
        }
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_category_403(self):
        """Test patch category got 403(No Permission)"""
        self.client.force_authenticate(self.no_permission_user)
        url = self.get_url(self.product.id)
        payload = {
            'name': '403'
        }
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_category_404(self):
        """Test patch category got 404(Not found product)"""
        self.client.force_authenticate(self.superuser)
        url = self.get_url(12341)
        payload = {
            'name': '404'
        }
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_category_invalid_type_400(self):
        """Test patch category got 400(Invalid type in payload)"""
        self.client.force_authenticate(self.superuser)
        url = self.get_url(self.product.id)
        payload = {
            'name': {'400': 'Invalid type'}
        }
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_category_no_mandatory_200(self):
        """Test patch category got 200(no mandatory)"""
        self.client.force_authenticate(self.superuser)
        url = self.get_url(self.product.id)
        payload = {
            'description': 'No name ,no category'
        }
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
