from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.utils_test import sample_user, sample_category, \
    sample_super_group


class PublicCategoryPutApiTest(TestCase):
    """Public tests suits for Category Put API"""

    @staticmethod
    def get_url(category_id):
        return reverse('category:category-put', args=[category_id])

    def setUp(self):
        self.user = sample_user()
        sample_super_group(user=self.user)
        self.category = sample_category(user=self.user)
        self.client = APIClient()

    def test_category_put_401(self):
        """Test category put api got 401(Unauthenticated)"""
        payload = {
            'name': '401'
        }
        url = self.get_url(self.category.id)
        res = self.client.put(path=url, data=payload, fromat='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_put_category_not_found_401(self):
        """Test category put api got 401(Unauthenticated)"""
        payload = {
            'name': '401'
        }
        url = self.get_url(10000000000)
        res = self.client.put(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryPutApiTest(TestCase):
    """Private tests suits for Category Put API"""

    @staticmethod
    def get_url(category_id):
        return reverse('category:category-put', args=[category_id])

    def setUp(self):
        self.user = sample_user()
        self.user2 = sample_user(email="NoPermission@test.com")
        sample_super_group(user=self.user)
        self.category = sample_category(user=self.user)
        self.client = APIClient()

    def test_category_put_200(self):
        """Test category put api got 200(Successful)"""
        self.client.force_authenticate(self.user)
        payload = {
            'name': '200'
        }
        url = self.get_url(self.category.id)
        res = self.client.put(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['updated_by'], self.user.id)

    def test_category_put_not_found_id_200(self):
        """Test category put api not found ID 200(Successful)"""
        self.client.force_authenticate(self.user)
        payload = {
            'name': '200'
        }
        url = self.get_url(1100000)
        res = self.client.put(path=url, data=payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # TODO: Check why put not get right ID
        # self.assertEqual(res.data['id'], 1100000)
        self.assertEqual(res.data['created_by'], self.user.id)
        self.assertEqual(res.data['updated_by'], self.user.id)

    def test_category_put_403(self):
        """Test category put api got 403(No Permission"""
        self.client.force_authenticate(self.user2)
        payload = {
            'name': '403'
        }
        url = self.get_url(self.category.id)
        res = self.client.put(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_put_not_found_id_403(self):
        """Test category put api not found id got 403(No Permission)"""
        self.client.force_authenticate(self.user2)
        payload = {
            'name': '403'
        }
        url = self.get_url(100000)
        res = self.client.put(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_put_invalid_type_400(self):
        """Test category api put invalid type in payload got 400(Bad Request)"""
        self.client.force_authenticate(self.user)
        payload = {
            'name': {'400': 'Dictionary instead of String'}
        }
        url = self.get_url(self.category.id)
        res = self.client.put(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_put_missing_mandatory_400(self):
        """Test category api put missing mandatory(name) got 400(Bad Request)"""
        self.client.force_authenticate(self.user)
        payload = {
            'status': 4
        }
        url = self.get_url(self.category.id)
        res = self.client.put(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_put_not_found_id_invalid_type_400(self):
        """Test category api put invalid type - not found id got 400"""
        self.client.force_authenticate(self.user)
        payload = {
            'name': {'400': 'Dictionary instead of String'}
        }
        url = self.get_url(1000000)
        res = self.client.put(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_put_not_found_id_missing_mandatory_400(self):
        """Test category api put missing mandatory(name) - not found id  got
        400(Bad Request)"""
        self.client.force_authenticate(self.user)
        payload = {
            'status': 4
        }
        url = self.get_url(1000000)
        res = self.client.put(path=url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
