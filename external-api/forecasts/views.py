from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ForecastDaySerializer
from .services import get_forecast


class WeatherForecastView(APIView):
    """Retorna a previsão do tempo para os próximos N dias de uma cidade."""

    def get(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({'error': 'O parâmetro "city" é obrigatório.'}, status=400)

        days = int(request.query_params.get('days', 5))
        forecast = get_forecast(city, days)
        serializer = ForecastDaySerializer(forecast, many=True)
        return Response(serializer.data)