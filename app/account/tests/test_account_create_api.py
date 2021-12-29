from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from unittest import mock

ACCOUNT_CREATE_URL = reverse('account:create-user')


class AccountCreateApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_201(self):
        """Test create user got 201(Created)"""
        payload = {
            'email': 'Test_200@gmail.com',
            'password': 'Testing123',
            'name': 'Test 200'
        }
        with mock.patch('account.utils.Util.send_mail', return_value=None):
            res = self.client.post(ACCOUNT_CREATE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_user_missing_mandatory_400(self):
        """Test create user missing mandatory got 400(Bad Request)"""
        payload = {
            'email': 'Test_200@gmail.com'
        }
        with mock.patch('account.utils.Util.send_mail', return_value=None):
            res = self.client.post(ACCOUNT_CREATE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
