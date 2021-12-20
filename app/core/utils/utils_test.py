from django.contrib.auth import get_user_model


def sample_user(*, email="UT@nhat.com", password="123456", name="Unit Test"):
    """Create a sample user"""
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
        name=name
    )
    return user
