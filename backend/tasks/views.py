from rest_framework.decorators import action
from rest_framework.response import Response

from .services import WeatherServiceError, get_weather_suggestion

from django.db.models import Q
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de tarefas.

    Um usuário vê tarefas que ele criou OU que foram compartilhadas com ele.
    Suporta filtragem (?is_completed=true, ?priority=high, ?category=1) e
    paginação (herdada da configuração global em settings.py).
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_completed', 'priority', 'category']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(owner=user) | Q(shared_with=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], url_path='weather-suggestion')
    def weather_suggestion(self, request, pk=None):
        """Retorna a previsão do tempo e o melhor dia para tarefas outdoor."""
        task = self.get_object()

        if not task.is_outdoor:
            return Response(
                {'error': 'Esta tarefa não está marcada como atividade outdoor.'},
                status=400,
            )
        if not task.city:
            return Response(
                {'error': 'Esta tarefa não possui uma cidade definida.'},
                status=400,
            )

        try:
            suggestion = get_weather_suggestion(task.city)
        except WeatherServiceError as exc:
            return Response({'error': str(exc)}, status=502)

        return Response(suggestion)