from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer usado para exibir dados do usuário (sem senha)."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer usado para criar um novo usuário com senha validada."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']

    def create(self, validated_data):
        # set_password garante o hash correto da senha (nunca salvar em texto puro)
        user = User.objects.create_user(**validated_data)
        return user