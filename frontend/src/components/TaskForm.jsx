import { useState } from "react";

export default function TaskForm({ categories, onSubmit }) {
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState("medium");
  const [categoryId, setCategoryId] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    if (!title.trim()) return;

    await onSubmit({
      title,
      priority,
      category: categoryId || null,
    });

    setTitle("");
    setPriority("medium");
    setCategoryId("");
  }

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <input
        type="text"
        placeholder="Nova tarefa..."
        value={title}
        onChange={(event) => setTitle(event.target.value)}
        required
      />

      <select
        value={priority}
        onChange={(event) => setPriority(event.target.value)}
      >
        <option value="low">Baixa</option>
        <option value="medium">Média</option>
        <option value="high">Alta</option>
      </select>

      <select
        value={categoryId}
        onChange={(event) => setCategoryId(event.target.value)}
      >
        <option value="">Sem categoria</option>
        {categories.map((category) => (
          <option key={category.id} value={category.id}>
            {category.name}
          </option>
        ))}
      </select>

      <button type="submit">Adicionar</button>
    </form>
  );
}
