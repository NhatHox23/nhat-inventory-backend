# from django.test import TestCase
# from django.urls import reverse
#
# from rest_framework.test import APIClient
# from rest_framework import status
#
# from core.utils.utils_test import sample_user
#
# CATEGORY_URL = reverse('category:list-category')
#
#
# class PublicCategoryApiTest(TestCase):
#     """Test Category api without log-in"""
#
#     def setUp(self):
#         self.user = sample_user()
#         self.client = APIClient()
#
#     def test_list_category_unauthenticated(self):
#         """Test that list category with status 401"""
#         res = self.client.get(CATEGORY_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class PrivateCategoryApiTest(TestCase):
#     """Test Category api with log-in"""
#
#     def setUp(self):
#         self.user = sample_user()
#         self.client = APIClient()
#         self.client.force_authenticate(self.user)
#
#     def test_list_category_successful(self):
#         res = self.client.get(CATEGORY_URL)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
