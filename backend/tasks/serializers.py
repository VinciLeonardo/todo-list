from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'is_completed', 'priority',
            'due_date', 'owner', 'category', 'shared_with',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def validate_category(self, category):
        """Garante que o usuário só use categorias próprias."""
        request = self.context['request']
        if category and category.owner != request.user:
            raise serializers.ValidationError('Categoria inválida para este usuário.')
        return category