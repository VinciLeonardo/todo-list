from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Endpoint público de cadastro de novos usuários.

    O login em si é feito pelo endpoint padrão do simplejwt (TokenObtainPairView),
    então essa view cuida apenas da criação da conta.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserListView(generics.ListAPIView):
    """Lista usuários para compartilhamento, excluindo o usuário autenticado."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)