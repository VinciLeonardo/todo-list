from rest_framework import viewsets, permissions

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de categorias.

    Cada usuário só vê e gerencia as próprias categorias (queryset filtrado
    por owner). Usar ViewSet aqui evita repetir código de List/Create/Update/
    Delete (princípio DRY) já que o padrão CRUD é o mesmo em toda a app.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)