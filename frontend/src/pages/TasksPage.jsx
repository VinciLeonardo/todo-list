import { useAuth } from "../contexts/AuthContext";

export default function TasksPage() {
  const { logout } = useAuth();

  return (
    <div>
      <h1>Minhas Tarefas</h1>
      <p>Em construção...</p>
      <button onClick={logout}>Sair</button>
    </div>
  );
}
