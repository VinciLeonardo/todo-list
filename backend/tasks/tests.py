import pytest
from django.urls import reverse
from rest_framework import status

from .models import Task


@pytest.mark.django_db
class TestTaskCRUD:
    def test_create_task(self, auth_client):
        url = reverse('task-list')
        response = auth_client.post(url, {'title': 'Estudar Django'})

        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 1

    def test_mark_task_as_completed(self, auth_client, user):
        task = Task.objects.create(title='Tarefa', owner=user)
        url = reverse('task-detail', args=[task.id])

        response = auth_client.patch(url, {'is_completed': True})

        task.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert task.is_completed is True

    def test_filter_by_completed_status(self, auth_client, user):
        Task.objects.create(title='Feita', owner=user, is_completed=True)
        Task.objects.create(title='Pendente', owner=user, is_completed=False)

        url = reverse('task-list')
        response = auth_client.get(url, {'is_completed': 'true'})

        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == 'Feita'

    def test_user_sees_tasks_shared_with_them(self, auth_client, user, other_user):
        task = Task.objects.create(title='Compartilhada', owner=other_user)
        task.shared_with.add(user)

        url = reverse('task-list')
        response = auth_client.get(url)

        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == 'Compartilhada'

    def test_user_does_not_see_tasks_of_other_users(self, auth_client, other_user):
        Task.objects.create(title='Não deveria aparecer', owner=other_user)

        url = reverse('task-list')
        response = auth_client.get(url)

        assert response.data['count'] == 0