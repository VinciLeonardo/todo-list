# To-Do List Avançado

Aplicação web de gerenciamento de tarefas com categorias, compartilhamento entre
usuários, autenticação, filtros, paginação e integração com uma API externa de
previsão do tempo.

## Arquitetura

- **backend/**: Django + Django REST Framework — API principal (usuários, tarefas, categorias, compartilhamento)
- **frontend/**: React (Vite) — interface web
- **external-api/**: Django REST Framework — API externa de previsão do tempo, consumida pelo backend

## Status
- [x] Estrutura inicial do repositório
- [ ] Backend
- [ ] Frontend
- [ ] Docker
- [ ] Testes
- [ ] CI/CD