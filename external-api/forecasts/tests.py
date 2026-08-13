from datetime import date

import pytest

from .services import CONDITIONS, get_forecast


class TestGetForecast:
    def test_returns_requested_number_of_days(self):
        forecast = get_forecast('Araranguá', days=5)
        assert len(forecast) == 5

    def test_first_day_is_today(self):
        forecast = get_forecast('Araranguá', days=1)
        assert forecast[0]['date'] == date.today().isoformat()

    def test_forecast_is_deterministic_for_same_city_and_day(self):
        """Mesma cidade, mesmo dia = mesma previsão (facilita testes e cache)."""
        forecast_1 = get_forecast('Florianópolis', days=3)
        forecast_2 = get_forecast('Florianópolis', days=3)
        assert forecast_1 == forecast_2

    def test_different_cities_can_have_different_forecasts(self):
        forecast_a = get_forecast('São Paulo', days=3)
        forecast_b = get_forecast('Rio de Janeiro', days=3)
        assert forecast_a != forecast_b

    def test_condition_is_always_valid(self):
        forecast = get_forecast('Curitiba', days=10)
        for day in forecast:
            assert day['condition'] in CONDITIONS

    def test_good_for_outdoor_matches_condition(self):
        forecast = get_forecast('Porto Alegre', days=10)
        for day in forecast:
            if day['condition'] == 'chuvoso':
                assert day['good_for_outdoor'] is False
            else:
                assert day['good_for_outdoor'] is True


@pytest.mark.django_db
class TestWeatherForecastView:
    def test_requires_city_parameter(self, client):
        response = client.get('/api/weather/')
        assert response.status_code == 400

    def test_returns_forecast_for_valid_city(self, client):
        response = client.get('/api/weather/', {'city': 'Araranguá', 'days': 3})
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_default_days_is_five(self, client):
        response = client.get('/api/weather/', {'city': 'Araranguá'})
        assert len(response.json()) == 5