import { useState } from "react";

export default function TaskForm({ categories, onSubmit }) {
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState("medium");
  const [categoryId, setCategoryId] = useState("");
  const [isOutdoor, setIsOutdoor] = useState(false);
  const [city, setCity] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    if (!title.trim()) return;

    await onSubmit({
      title,
      priority,
      category: categoryId || null,
      is_outdoor: isOutdoor,
      city: isOutdoor ? city.trim() : "",
    });

    setTitle("");
    setPriority("medium");
    setCategoryId("");
    setIsOutdoor(false);
    setCity("");
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

      <label className="task-outdoor-field">
        <input
          type="checkbox"
          checked={isOutdoor}
          onChange={(event) => {
            const checked = event.target.checked;
            setIsOutdoor(checked);
            if (!checked) setCity("");
          }}
        />
        É uma atividade externa?
      </label>

      {isOutdoor && (
        <input
          type="text"
          placeholder="Cidade"
          value={city}
          onChange={(event) => setCity(event.target.value)}
        />
      )}

      <button type="submit">Adicionar</button>
    </form>
  );
}
