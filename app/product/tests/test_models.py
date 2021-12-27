from django.db import IntegrityError
from django.test import TestCase
from product.models import Product

from core.utils.utils_test import sample_user, sample_category


class ProductModelTest(TestCase):
    """Test suits for product model"""

    def setUp(self):
        self.user = sample_user()
        self.category = sample_category(user=self.user)

    def test_product_string(self):
        """Test that string representation return product name"""
        product = Product.objects.create(
            name="Test Product",
            status=0,
            price=10000,
            category=self.category
        )
        self.assertEqual(str(product), product.name)

    def test_product_duplicate_name(self):
        """Test that product with same category can't have same name"""
        Product.objects.create(
            name="Test Product",
            status=0,
            price=10000,
            category=self.category
        )
        with self.assertRaises(IntegrityError) as raises:
            Product.objects.create(
                name="Test Product",
                status=0,
                price=10000,
                category=self.category
            )
        self.assertEqual(IntegrityError, type(raises.exception))
