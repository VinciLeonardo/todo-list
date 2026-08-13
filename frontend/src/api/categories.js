import apiClient from "./client";

export async function listCategories() {
  const response = await apiClient.get("/categories/");
  return response.data;
}

export async function createCategory(data) {
  const response = await apiClient.post("/categories/", data);
  return response.data;
}
