import { useEffect, useState } from "react";
import { getWeatherSuggestion } from "../api/tasks";

// Maps a temperature onto a cold (sky blue) → warm (amber) hue
// scale, so the forecast list reads at a glance like a real
// weather strip instead of a plain table of numbers.
function temperatureColor(celsius) {
  const clamped = Math.max(0, Math.min(35, celsius));
  const ratio = clamped / 35;
  const hue = 205 - ratio * 175; // 205 (sky) -> 30 (amber)
  return `hsl(${hue}, 42%, 45%)`;
}

export default function WeatherSuggestionModal({ task, onClose }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [forecast, setForecast] = useState([]);
  const [bestDay, setBestDay] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadWeatherSuggestion() {
      setLoading(true);
      setError("");
      try {
        const data = await getWeatherSuggestion(task.id);
        if (!isMounted) return;
        setForecast(data.forecast || []);
        setBestDay(data.best_day);
      } catch (err) {
        if (!isMounted) return;
        setError(
          err.response?.data?.error ||
            "Não foi possível carregar a previsão do tempo.",
        );
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    loadWeatherSuggestion();

    return () => {
      isMounted = false;
    };
  }, [task.id]);

  return (
    <div className="share-task-modal" role="dialog" aria-modal="true">
      <div className="share-task-modal-content">
        <h3>Previsão do tempo: {task.title}</h3>
        {task.city && <p className="weather-city">Cidade: {task.city}</p>}

        {loading ? (
          <p>Carregando previsão...</p>
        ) : (
          <>
            {error && <p className="error-message">{error}</p>}

            {!error && (
              <>
                {bestDay ? (
                  <div className="weather-best-day">
                    <h4>Melhor dia</h4>
                    <p>
                      {bestDay.date} - {bestDay.condition} -{" "}
                      {bestDay.temperature_celsius}°C
                    </p>
                  </div>
                ) : (
                  <p>Nenhum dia bom previsto nos próximos dias.</p>
                )}

                <h4>Previsão completa</h4>
                <ul className="weather-forecast-list">
                  {forecast.map((day) => (
                    <li key={day.date} className="weather-forecast-item">
                      <span
                        className="temp-dot"
                        style={{
                          background: temperatureColor(
                            day.temperature_celsius,
                          ),
                        }}
                      />
                      <span className="forecast-date">{day.date}</span>
                      <span className="forecast-condition">
                        {day.condition}
                      </span>
                      <span className="forecast-temp">
                        {day.temperature_celsius}°C
                      </span>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </>
        )}

        <div className="share-task-actions">
          <button type="button" onClick={onClose}>
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
}
