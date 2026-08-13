import hashlib
import random
from datetime import date, timedelta

CONDITIONS = ['ensolarado', 'nublado', 'chuvoso', 'parcialmente nublado']


def get_forecast(city: str, days: int = 5):
    """
    Gera uma previsão do tempo simulada, porém determinística.

    Usamos o nome da cidade + a data como seed, então a mesma cidade sempre
    retorna a mesma previsão para o mesmo dia (útil para testes automatizados
    reproduzíveis, sem depender de uma API externa real com limites de uso).
    """
    forecast = []
    today = date.today()

    for i in range(days):
        current_day = today + timedelta(days=i)
        seed = f'{city.lower()}-{current_day.isoformat()}'
        seed_hash = int(hashlib.md5(seed.encode()).hexdigest(), 16)
        rng = random.Random(seed_hash)

        condition = rng.choice(CONDITIONS)
        forecast.append({
            'date': current_day.isoformat(),
            'condition': condition,
            'temperature_celsius': rng.randint(12, 34),
            'good_for_outdoor': condition != 'chuvoso',
        })

    return forecast