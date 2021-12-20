from rest_framework import viewsets

from rest_framework.response import Response

from rest_framework import status

from .models import Category

from rest_framework import permissions


class CategoryApiViewSet(viewsets.ModelViewSet):
    """Category API Viewset"""
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        return Response({"hello": "World"}, status=status.HTTP_200_OK)
