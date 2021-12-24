from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission


def sample_super_group(*, user=None):
    """Create a full permission"""
    permission_list = [permission.id for permission in Permission.objects.all()]
    group = Group.objects.create(name="superuser")
    group.permissions.add(*permission_list)
    if user:
        user.groups.add(group)
    return group


def sample_user(*, email="UT@nhat.com", password="123456", name="Unit Test"):
    """Create a sample user"""
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
        name=name
    )
    return user
