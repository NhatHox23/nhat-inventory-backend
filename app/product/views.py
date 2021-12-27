from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.utils.utils_permission import DjangoModelPermissionSafeMethod
from core.utils.utils_query import get_or_404

from .models import Product
from .serializers import ProductSerializer


class ProductViewSetAPI(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissionSafeMethod,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @swagger_auto_schema(
        operation_id="List Product API",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="OK",
                schema=ProductSerializer(many=True, )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="UnAuthenticated"
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="No Permission"
            )
        }
    )
    def list(self, request, *args, **kwargs):
        """
        List Product API

        ### Description:
            - This API serve the purpose of listing product
        ### Permission:
            - Can view Product
        """
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="Create Product API",
        request_body=ProductSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='OK',
                schema=ProductSerializer
            ),
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
        """
        Create Product API

        ### Description:
            - This API serve the purpose of creating product
        ### Permission:
            - Can add Product
        """
        user = request.user.id
        data = request.data
        data["created_by"] = user
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_id="Put Product API",
        request_body=ProductSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='OK',
                schema=ProductSerializer()
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description='UnAuthenticated'
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description='No Permission'
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='Not Found'
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='Bad Request'
            )
        }
    )
    def update(self, request, product_id, *args, **kwargs):
        """
        Put Product API

        ### Description:
            - This API serve the purpose of update(PUT) product

        ### Permission:
            - Can change Product
        """
        user = request.user.id
        data = request.data
        data["updated_by"] = user
        product = get_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="Patch Product API",
        request_body=ProductSerializer(partial=False),
        response={
            status.HTTP_200_OK: openapi.Response(
                description='OK',
                schema=ProductSerializer()
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Unauthenticated'
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description='No Permission'
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='Not Found'
            )
        }
    )
    def partial_update(self, request, product_id, *args, **kwargs):
        """
        Patch Product API

        ### Description:
            - This API serve the purpose of update(PATCH) product

        ### Permission:
            - Can change Product
        """
        user = request.user.id
        data = request.data
        data['updated_by'] = user
        product = get_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
