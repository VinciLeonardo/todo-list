import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { listCategories, createCategory } from "../api/categories";
import CategoryForm from "../components/CategoryForm";

export default function CategoriesPage() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadCategories = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await listCategories();
      setCategories(data.results);
    } catch {
      setError("Não foi possível carregar as categorias.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCategories();
  }, [loadCategories]);

  async function handleCreate(categoryData) {
    await createCategory(categoryData);
    loadCategories();
  }

  return (
    <div className="categories-page">
      <header>
        <h1>Categorias</h1>
        <Link to="/tasks">Voltar para tarefas</Link>
      </header>

      <CategoryForm onSubmit={handleCreate} />

      {error && <p className="error-message">{error}</p>}

      {loading ? (
        <p>Carregando...</p>
      ) : (
        <ul className="category-list">
          {categories.map((category) => (
            <li key={category.id} className="category-item">
              <span
                className="category-color-dot"
                style={{ backgroundColor: category.color }}
              />
              {category.name}
            </li>
          ))}
          {categories.length === 0 && <p>Nenhuma categoria cadastrada.</p>}
        </ul>
      )}
    </div>
  );
}
