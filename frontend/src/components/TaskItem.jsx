import { useState } from "react";
import ShareTaskModal from "./ShareTaskModal";
import WeatherSuggestionModal from "./WeatherSuggestionModal";

export default function TaskItem({ task, onToggleComplete, onDelete, onShared }) {
  const [isSharing, setIsSharing] = useState(false);
  const [isWeatherOpen, setIsWeatherOpen] = useState(false);

  return (
    <>
      <li className={`task-item ${task.is_completed ? "completed" : ""}`}>
        <label>
          <input
            type="checkbox"
            checked={task.is_completed}
            onChange={() => onToggleComplete(task)}
          />
          <span className="task-title">{task.title}</span>
        </label>

        {task.priority && (
          <span className={`badge priority-${task.priority}`}>
            {task.priority}
          </span>
        )}
        {task.due_date && <span className="task-due-date">{task.due_date}</span>}

        {task.is_outdoor && (
          <button type="button" onClick={() => setIsWeatherOpen(true)}>
            Ver previsão do tempo
          </button>
        )}
        <button type="button" onClick={() => setIsSharing(true)}>
          Compartilhar
        </button>
        <button
          type="button"
          onClick={() => onDelete(task.id)}
          className="delete-button"
        >
          Excluir
        </button>
      </li>

      {isSharing && (
        <ShareTaskModal
          task={task}
          onShared={onShared}
          onClose={() => setIsSharing(false)}
        />
      )}
      {isWeatherOpen && (
        <WeatherSuggestionModal
          task={task}
          onClose={() => setIsWeatherOpen(false)}
        />
      )}
    </>
  );
}
