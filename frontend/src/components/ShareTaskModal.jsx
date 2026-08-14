import { useEffect, useState } from "react";
import { listShareableUsers, shareTask } from "../api/tasks";

function normalizeSharedWith(sharedWith = []) {
  return sharedWith
    .map((value) => (typeof value === "object" ? value.id : value))
    .filter(Boolean);
}

export default function ShareTaskModal({ task, onClose, onShared }) {
  const [users, setUsers] = useState([]);
  const [selectedUserIds, setSelectedUserIds] = useState(
    normalizeSharedWith(task.shared_with),
  );
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadUsers() {
      setLoading(true);
      setError("");
      try {
        const data = await listShareableUsers();
        setUsers(data.results);
      } catch {
        setError("Não foi possível carregar os usuários.");
      } finally {
        setLoading(false);
      }
    }

    loadUsers();
  }, []);

  function handleToggleUser(userId) {
    setSelectedUserIds((previousIds) => {
      if (previousIds.includes(userId)) {
        return previousIds.filter((id) => id !== userId);
      }
      return [...previousIds, userId];
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    setError("");

    try {
      await shareTask(task.id, selectedUserIds);
      await onShared();
      onClose();
    } catch {
      setError("Não foi possível compartilhar a tarefa.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="share-task-modal" role="dialog" aria-modal="true">
      <div className="share-task-modal-content">
        <h3>Compartilhar: {task.title}</h3>

        {error && <p className="error-message">{error}</p>}

        {loading ? (
          <p>Carregando usuários...</p>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="share-users-list">
              {users.map((user) => (
                <label key={user.id} className="share-user-option">
                  <input
                    type="checkbox"
                    checked={selectedUserIds.includes(user.id)}
                    onChange={() => handleToggleUser(user.id)}
                  />
                  <span>
                    {user.username} ({user.email})
                  </span>
                </label>
              ))}
            </div>

            {users.length === 0 && (
              <p className="share-empty-state">Nenhum usuário disponível.</p>
            )}

            <div className="share-task-actions">
              <button type="button" onClick={onClose} disabled={saving}>
                Cancelar
              </button>
              <button type="submit" disabled={saving}>
                {saving ? "Salvando..." : "Salvar compartilhamento"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
