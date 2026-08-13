import { useState } from "react";

export default function CategoryForm({ onSubmit }) {
  const [name, setName] = useState("");
  const [color, setColor] = useState("#3B82F6");

  async function handleSubmit(event) {
    event.preventDefault();
    if (!name.trim()) return;

    await onSubmit({ name, color });
    setName("");
    setColor("#3B82F6");
  }

  return (
    <form onSubmit={handleSubmit} className="category-form">
      <input
        type="text"
        placeholder="Nova categoria..."
        value={name}
        onChange={(event) => setName(event.target.value)}
        required
      />
      <input
        type="color"
        value={color}
        onChange={(event) => setColor(event.target.value)}
      />
      <button type="submit">Adicionar</button>
    </form>
  );
}
