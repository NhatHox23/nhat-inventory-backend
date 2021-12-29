from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from category.models import Category

from product.models import Product


def sample_super_group(*, user=None):
    """Create a full permission"""
    permission_list = [permission.id for permission in Permission.objects.all()]
    group = Group.objects.create(name="superuser")
    group.permissions.add(*permission_list)
    if user:
        user.groups.add(group)
    return group


def sample_user(*, email="UT@nhat.com", password="123456", name="Unit Test",
                is_active=True):
    """Create a sample user"""
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
        name=name,
        is_active=is_active
    )
    return user


def sample_category(*, user=None, name='Sample Category', **kwargs):
    """Create a sample category"""
    category = Category.objects.create(name=name, created_by=user, **kwargs)
    return category


def sample_product(*, user=None, name='Sample Product', category, **kwargs):
    """Create a sample product"""
    product = Product.objects.create(name=name, category=category,
                                     created_by=user, **kwargs)
    return product
