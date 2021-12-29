from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from rest_framework import status
from rest_framework.test import APIClient

from rest_framework_simplejwt.tokens import RefreshToken

from core.utils.sample_test import sample_user
from account.models import User


class PublicUserVerifyApiTest(TestCase):
    """Public test suits for User Verify API"""

    @staticmethod
    def get_url(token=None):
        if token:
            return reverse('account:verify-email') + '?' + urlencode(
                {'token': token})
        else:
            return reverse('account:verify-email')

    @staticmethod
    def get_token(user):
        user = User.objects.get(id=user.id)
        return RefreshToken.for_user(user).access_token

    def setUp(self):
        self.user = sample_user(is_active=False)
        self.client = APIClient()

    def test_verify_email_200(self):
        """Test verify email got 200(Successful)"""
        token = self.get_token(user=self.user)
        url = self.get_url(token=token)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_verify_email_invalid_token_400(self):
        """Test verify email got 400(invalid token)"""
        token = "InvalidToken"
        url = self.get_url(token=token)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email_missing_token_400(self):
        """Test verify email got 400(missing token)"""
        url = self.get_url(token=None)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
