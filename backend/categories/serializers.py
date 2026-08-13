from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'owner', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']