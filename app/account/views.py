from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

import jwt

from .models import User
from .utils import Util
from .serializers import UserProfileSerializer, UserCreationSerializer
from core.utils.email import concat_link, get_token, send_mail


class UserSelfProfileApi(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_id="Detail Self Profile API",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Success', schema=UserProfileSerializer
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description='Unauthenticated'
            )
        }
    )
    def list(self, request, *args, **kwargs):
        """View Self Profile API
        ### Description:
            - This API serve the purpose of viewing self information
        ### Permission:
            - IsAuthenticated
        """
        user_id = request.user.id
        user_data = User.objects.get(id=user_id)
        serializer = UserProfileSerializer(user_data)
        return Response(serializer.data, status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        user_id = request.user.id
        user_data = User.objects.get(id=user_id)
        serializer = UserProfileSerializer(user_data, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        request_body=UserCreationSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                'Success', UserCreationSerializer(),
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                'Authenticated Failed'
            )
        }
    )
    def create(self, request, *args, **kwargs):
        user = request.data
        serializer = UserCreationSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = serializer.data
        user = User.objects.get(email=user['email'])
        token = get_token(user.id)
        current_site = get_current_site(request)
        relative_link = reverse('account:verify-email')
        abs_url = concat_link(current_site.domain, relative_link,
                              token=token.access_token)

        email_body = f'Hi {user.email} + Use link below to verify your ' \
                     f'email \n' + abs_url
        data = {
            'email_body': email_body,
            'subject': 'Welcome to N-Ecosystem',
            'domain': current_site.domain,
            'to_email': [user.email],
        }
        Util.send_mail(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(viewsets.ModelViewSet):

    def list(self, request):
        user_token = request.query_params.get('token', None)
        try:
            payload = jwt.decode(user_token, settings.SIMPLE_JWT[
                'SIGNING_KEY'], settings.SIMPLE_JWT['ALGORITHM'])
            user = User.objects.get(id=payload['user_id'])
            user.is_active = True
            user.save()
            return Response({user.email: "Is activated"},
                            status=status.HTTP_200_OK)
        except (jwt.InvalidSignatureError,
                jwt.DecodeError,
                jwt.ExpiredSignatureError, User.DoesNotExist):
            return Response({'message': 'invalid token or link'},
                            status=status.HTTP_400_BAD_REQUEST)
