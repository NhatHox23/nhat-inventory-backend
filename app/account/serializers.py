from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Permission, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "name", "password", "is_staff", "is_active")
        extra_kwargs = {
            "is_superuser": {"read_only": True},
            "is_staff": {"read_only": True},
            "email": {"read_only": True},
            "password": {"read_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        # extra_kwargs = {
        #     "name": {"required": False}
        # }
        #
