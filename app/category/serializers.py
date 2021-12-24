from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializers for Category model"""

    class Meta:
        model = Category
        fields = ("name", "status", "created_by", "updated_by")
