import pytest
from django.urls import reverse
from rest_framework import status

from .models import Category


@pytest.mark.django_db
class TestCategoryCRUD:
    def test_create_category(self, auth_client):
        url = reverse('category-list')
        response = auth_client.post(url, {'name': 'Trabalho', 'color': '#EF4444'})

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == 1

    def test_list_only_returns_own_categories(self, auth_client, user, other_user):
        Category.objects.create(name='Minha', owner=user)
        Category.objects.create(name='De outro', owner=other_user)

        url = reverse('category-list')
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == 'Minha'

    def test_unauthenticated_user_cannot_access(self, api_client):
        url = reverse('category-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED