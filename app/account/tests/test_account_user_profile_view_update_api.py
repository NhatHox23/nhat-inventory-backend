from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.utils.sample_test import sample_user

SELF_USER_PROFILE_ULR = reverse('account:detail-self-user')


class PublicUserProfileApiTest(TestCase):
    """Public test suits for User Profile API"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()

    def test_get_profile_401(self):
        """Test get profile got 401(Unauthenticated)"""
        res = self.client.get(SELF_USER_PROFILE_ULR)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_401(self):
        """Test update profile got 401(Unauthenticated)"""
        payload = {
            'name': 'update 401'
        }
        res = self.client.patch(SELF_USER_PROFILE_ULR, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserProfileApiTest(TestCase):
    """Private test suits for User Profile API"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_profile_200(self):
        """Test get profile got 200(Successful)"""
        res = self.client.get(SELF_USER_PROFILE_ULR)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_profile_200(self):
        """Test update profile got 200(Successful)"""
        payload = {
            'name': 'update 200'
        }
        res = self.client.patch(SELF_USER_PROFILE_ULR, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_profile_400(self):
        """Test update profile got 400(invalid payload)"""
        payload = {
            'name': {'400': 'Dictionary instead of string'}
        }
        res = self.client.patch(SELF_USER_PROFILE_ULR, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
