import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { listTasks, createTask, updateTask, deleteTask } from "../api/tasks";
import { listCategories } from "../api/categories";
import TaskItem from "../components/TaskItem";
import TaskForm from "../components/TaskForm";

export default function TasksPage() {
  const { logout } = useAuth();

  const [tasks, setTasks] = useState([]);
  const [categories, setCategories] = useState([]);
  const [count, setCount] = useState(0);
  const [page, setPage] = useState(1);
  const [statusFilter, setStatusFilter] = useState("all"); // all | completed | pending
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadTasks = useCallback(async () => {
    setLoading(true);
    setError("");

    const params = { page };
    if (statusFilter === "completed") params.is_completed = true;
    if (statusFilter === "pending") params.is_completed = false;

    try {
      const data = await listTasks(params);
      setTasks(data.results);
      setCount(data.count);
    } catch {
      setError("Não foi possível carregar as tarefas.");
    } finally {
      setLoading(false);
    }
  }, [page, statusFilter]);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  useEffect(() => {
    listCategories()
      .then((data) => setCategories(data.results))
      .catch(() => {});
  }, []);

  async function handleCreate(taskData) {
    await createTask(taskData);
    setPage(1);
    loadTasks();
  }

  async function handleToggleComplete(task) {
    await updateTask(task.id, { is_completed: !task.is_completed });
    loadTasks();
  }

  async function handleDelete(taskId) {
    await deleteTask(taskId);
    loadTasks();
  }

  const pageSize = 10; // deve bater com o PAGE_SIZE do backend
  const totalPages = Math.ceil(count / pageSize);

  return (
    <div className="tasks-page">
      <header>
        <h1>Minhas Tarefas</h1>
        <Link to="/categories">Categorias</Link>
        <button onClick={logout}>Sair</button>
      </header>

      <TaskForm categories={categories} onSubmit={handleCreate} />

      <div className="filters">
        <button
          className={statusFilter === "all" ? "active" : ""}
          onClick={() => {
            setStatusFilter("all");
            setPage(1);
          }}
        >
          Todas
        </button>
        <button
          className={statusFilter === "pending" ? "active" : ""}
          onClick={() => {
            setStatusFilter("pending");
            setPage(1);
          }}
        >
          Pendentes
        </button>
        <button
          className={statusFilter === "completed" ? "active" : ""}
          onClick={() => {
            setStatusFilter("completed");
            setPage(1);
          }}
        >
          Concluídas
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}

      {loading ? (
        <p>Carregando...</p>
      ) : (
        <ul className="task-list">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDelete}
              onShared={loadTasks}
            />
          ))}
          {tasks.length === 0 && <p>Nenhuma tarefa encontrada.</p>}
        </ul>
      )}

      {totalPages > 1 && (
        <div className="pagination">
          <button disabled={page === 1} onClick={() => setPage((p) => p - 1)}>
            Anterior
          </button>
          <span>
            Página {page} de {totalPages}
          </span>
          <button
            disabled={page === totalPages}
            onClick={() => setPage((p) => p + 1)}
          >
            Próxima
          </button>
        </div>
      )}
    </div>
  );
}
