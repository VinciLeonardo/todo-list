import requests
from django.conf import settings


class WeatherServiceError(Exception):
    """Erro ao consultar a API externa de previsão do tempo."""


def get_weather_suggestion(city: str, days: int = 5):
    """
    Consulta a API externa de clima e retorna a previsão, já indicando
    qual é o melhor dia (primeiro dia bom) para uma atividade outdoor.
    """
    try:
        response = requests.get(
            settings.WEATHER_API_URL,
            params={'city': city, 'days': days},
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise WeatherServiceError(f'Não foi possível obter a previsão do tempo: {exc}')

    forecast = response.json()
    best_day = next((day for day in forecast if day['good_for_outdoor']), None)

    return {
        'forecast': forecast,
        'best_day': best_day,
    }