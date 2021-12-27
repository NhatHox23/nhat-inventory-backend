from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.utils.utils_permission import DjangoModelPermissionSafeMethod

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
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
