from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import UserProfileSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User


class UserViewSetApi(viewsets.ModelViewSet):
    """CRUD API for User"""
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
        operation_id="List User API",
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Success', UserProfileSerializer(many=True, )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Authenticated Failed"
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        """List out User API"""
        queryset = User.objects.all()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="Create User API",
        request_body=UserProfileSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                'Success', UserProfileSerializer(),
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                'AUthenticated Failed'
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
