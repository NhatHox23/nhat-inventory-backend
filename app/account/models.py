from django.db import models

from core.models import TimeStampModel

from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin

from django.utils.translation import gettext_lazy as _


# Create your models here.

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique for authentication
    """

    def create_user(self, email, password, **kwargs):
        """
        Create user with the given email and password
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create superuser with the given email and password
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser, TimeStampModel, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
