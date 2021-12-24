from rest_framework import viewsets, status
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.utils.utils_permission import DjangoModelPermissionSafeMethod

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSetAPI(viewsets.ModelViewSet):
    """Category ViewSet API
    ### Description:
        - Category ViewSet API

    ### Permission:
        - DjangoModelPermissionSafeMethod
    """
    permission_classes = [DjangoModelPermissionSafeMethod, ]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @swagger_auto_schema(
        operation_id='Category List API',
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='OK', schema=CategorySerializer(many=True, )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Unauthenticated'
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description='No Permission'
            )
        }
    )
    def list(self, request, *args, **kwargs):
        """List Category API"""
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id='Category Create API',
        request_body=CategorySerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='OK', schema=CategorySerializer()),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description='UnAuthenticated'
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description='No Permission'
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='Bad Request'
            )
        }
    )
    def create(self, request, *args, **kwargs):
        """Create Category API"""
        user = request.user.id
        data = request.data
        data["created_by"] = user
        serializer = CategorySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
