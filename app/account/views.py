from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserProfileSerializer, UserCreationSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


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
                'AUthenticated Failed'
            )
        }
    )
    def create(self, request, *args, **kwargs):
        user = request.data
        serializer = UserProfileSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user)

        current_site = get_current_site(request)
        relative_link = reverse('account:verify-email')

        absurl = 'http://' + current_site.domain + relative_link + "?token=" \
                 + str(token.access_token)
        email_body = f'Hi {user.email} + Use link below to verify your ' \
                     f'email \n' + absurl
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
        pass
