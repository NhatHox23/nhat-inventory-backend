from django.test import TestCase

from category.models import Category


class CategoryModelTest(TestCase):
    """Test Model Category"""

    def test_category_str_name(self):
        """Test string representation of category as category name"""
        category = Category.objects.create(
            name="Unit Test str()"
        )
        self.assertEqual(str(category), category.name)
