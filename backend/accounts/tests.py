import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestRegister:
    def test_register_creates_user(self, api_client):
        url = reverse('register')
        payload = {
            'username': 'carol',
            'email': 'carol@teste.com',
            'password': 'senha12345',
        }
        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username='carol').exists()
        # A senha nunca deve voltar na resposta
        assert 'password' not in response.data

    def test_register_fails_with_duplicate_username(self, api_client, user):
        url = reverse('register')
        payload = {
            'username': user.username,
            'email': 'novo@teste.com',
            'password': 'senha12345',
        }
        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    def test_login_returns_tokens(self, api_client, user):
        url = reverse('login')
        payload = {'username': user.username, 'password': 'senha12345'}
        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_fails_with_wrong_password(self, api_client, user):
        url = reverse('login')
        payload = {'username': user.username, 'password': 'senha_errada'}
        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED