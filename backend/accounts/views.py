from rest_framework import generics, permissions

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    Endpoint público de cadastro de novos usuários.

    O login em si é feito pelo endpoint padrão do simplejwt (TokenObtainPairView),
    então essa view cuida apenas da criação da conta.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer