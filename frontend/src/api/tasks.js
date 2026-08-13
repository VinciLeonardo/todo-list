import apiClient from "./client";

export async function listTasks(params = {}) {
  const response = await apiClient.get("/tasks/", { params });
  return response.data;
}

export async function createTask(data) {
  const response = await apiClient.post("/tasks/", data);
  return response.data;
}

export async function updateTask(id, data) {
  const response = await apiClient.patch(`/tasks/${id}/`, data);
  return response.data;
}

export async function deleteTask(id) {
  await apiClient.delete(`/tasks/${id}/`);
}
