from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuário customizado do sistema.

    Estende o AbstractUser padrão do Django para permitir futuras extensões
    (ex: avatar, preferências) sem precisar de migração destrutiva depois.
    """
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username