from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.utils_test import sample_user, sample_super_group

CATEGORY_CREATE_URL = reverse('category:category-create')


class PublicCategoryCreateApiTest(TestCase):
    """Public test suits for category API"""

    def setUp(self):
        self.user = sample_user()
        sample_super_group(user=self.user)
        self.client = APIClient()

    def test_category_create_401(self):
        """Test that create category got 401 (unAuthenticated)"""
        payload = {
            "name": "Unit test 401"
        }
        res = self.client.post(CATEGORY_CREATE_URL, data=payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryCreateApiTest(TestCase):
    """Private test suits for category API"""

    def setUp(self):
        self.user = sample_user()
        self.user2 = sample_user(email="NoPermission@test.com")
        sample_super_group(user=self.user)
        self.client = APIClient()

    def test_category_create_201(self):
        """Test that create category got 201 (Successful)"""
        payload = {
            "name": "201"
        }
        self.client.force_authenticate(self.user)
        res = self.client.post(path=CATEGORY_CREATE_URL, data=payload,
                               format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_category_create_403(self):
        """Test that create category got 403 (No Permission)"""
        payload = {
            "name": "403"
        }
        self.client.force_authenticate(self.user2)
        res = self.client.post(path=CATEGORY_CREATE_URL, data=payload,
                               format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_create_400_Empty_Payload(self):
        """Test that create category got 400 (Empty payload)"""
        payload = {}
        self.client.force_authenticate(self.user)
        res = self.client.post(path=CATEGORY_CREATE_URL, data=payload,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_create_400_Invalid_Type_Payload(self):
        """Test that create category got 400 (Invalid type in payload)"""
        payload = {
            "name": {"400": "Dictionary instead of String"}
        }
        self.client.force_authenticate(self.user)
        res = self.client.post(path=CATEGORY_CREATE_URL, data=payload,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
