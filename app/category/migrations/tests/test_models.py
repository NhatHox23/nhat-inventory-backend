from django.test import TestCase

from category.models import Category


class CategoryModelTest(TestCase):

    def test_category_str(self):
        """test string representation for category model"""
        test_name = "Unit test name"
        category = Category.objects.create(
            name=test_name,
            status=Category.AVALIABLE
        )
        self.assertEqual(str(category), test_name)

