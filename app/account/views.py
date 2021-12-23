from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import IsAuthenticated, IsAdminUser, \
    BasePermission, SAFE_METHODS
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import Group, Permission

from .serializers import PermissionSerializer, UserProfileSerializer, \
    GroupSerializer
from .models import User


class IsAdminUserOrReadOnly(BasePermission):
    """Allow for admin user, Read only for authenticated"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user:
            return True
        elif request.user and request.user.is_staff:
            return True
        else:
            return False


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['name'] = user.name

        # Add more field if wanted

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserProfileApiViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        

class PermissionApiViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = PermissionSerializer

    def list(self, request, *args, **kwargs):
        permission = Permission.objects.filter(id__gte=3).order_by("id")
        serializer = PermissionSerializer(permission, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupApiViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly, ]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def update(self, request, group_id, *args, **kwargs):
        group = Group.objects.get(id=group_id)
        # permission_list = request.data.get('permissions')
        # permissions_dict = {"permissions": request.data.get('permissions')}
        serializer = GroupSerializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_202_ACCEPTED)
