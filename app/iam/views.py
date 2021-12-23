from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, \
    DjangoModelPermissionsOrAnonReadOnly, \
    IsAuthenticatedOrReadOnly

from django.contrib.auth.models import Permission, Group

from .serializers import PermissionSerializer, GroupSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['name'] = user.name

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    """Token API"""
    serializer_class = MyTokenObtainPairSerializer


class MyRefreshTokenObtainPairView(TokenRefreshView):
    """Refresh API Token"""
    serializer_class = MyTokenObtainPairSerializer


class PermissionViewSetApi(viewsets.ModelViewSet):
    """Permission API"""
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all().order_by("id")


class GroupViewSetApi(viewsets.ModelViewSet):
    """Group API"""
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]
    serializer_class = GroupSerializer
    queryset = Group.objects.all().order_by("id")

