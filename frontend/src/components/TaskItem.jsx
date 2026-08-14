import { useState } from "react";
import ShareTaskModal from "./ShareTaskModal";

export default function TaskItem({ task, onToggleComplete, onDelete, onShared }) {
  const [isSharing, setIsSharing] = useState(false);

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
    </>
  );
}
