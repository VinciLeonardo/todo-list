# To-Do List Avançado

Aplicação web de gerenciamento de tarefas com categorias, compartilhamento
entre usuários, autenticação JWT, filtros, paginação e sugestão de melhor
dia para tarefas ao ar livre com base em uma API externa de previsão do
tempo.

Projeto full stack (Django REST Framework + React) desenvolvido como teste
técnico, cobrindo backend, frontend, integração entre serviços, testes
automatizados (unitários, de API e end-to-end) e containerização.

## Arquitetura

O projeto é dividido em três serviços independentes, orquestrados via Docker Compose:

```
┌──────────────┐      ┌──────────────────┐      ┌────────────────────┐
│   frontend   │ ───▶ │      backend      │ ───▶ │    external-api     │
│ React + Vite │      │  Django + DRF     │      │   Django + DRF      │
│  (porta 5173)│      │   (porta 8000)    │      │    (porta 8001)     │
└──────────────┘      └────────┬─────────┘      └────────────────────┘
                                │
                        ┌───────▼────────┐
                        │   PostgreSQL   │
                        │  (porta 5432)  │
                        └────────────────┘
```

- **backend/** Django + Django REST Framework. API principal: autenticação
  (JWT via `djangorestframework-simplejwt`), usuários, tarefas, categorias e
  compartilhamento de tarefas entre usuários. Consome a `external-api` para
  sugerir o melhor dia para tarefas outdoor.
- **frontend/** React (Vite). Interface web: login/cadastro, CRUD de
  tarefas e categorias, compartilhamento, filtros, paginação e visualização
  da previsão do tempo.
- **external-api/** Django REST Framework isolada, simulando uma API de
  previsão do tempo de terceiros. Separada da API principal para modelar
  uma integração real com um serviço externo (contrato HTTP próprio, sem
  acoplamento ao banco de dados do backend).

### Por que uma `external-api` separada?

Em vez de simular a previsão do tempo dentro do próprio backend, ela foi
isolada em um serviço HTTP à parte. Isso obriga o backend a consumir a
integração como consumiria qualquer API de terceiros de verdade (ex.:
OpenWeather) com timeout, tratamento de erro de rede
(`WeatherServiceError`) e um contrato de dados desacoplado em vez de
apenas chamar uma função Python local.

### Decisões de design

- **Autenticação por JWT** (access + refresh token) em vez de sessão, já
  que o frontend é uma SPA desacoplada do backend.
- **Compartilhamento de tarefas** via relação `ManyToMany` (`shared_with`),
  permitindo que uma tarefa pertença a um dono (`owner`) mas seja visível e
  editável por outros usuários selecionados.
- **Tarefas outdoor**: o campo `is_outdoor` + `city` no modelo `Task`
  aciona a consulta à `external-api`; o backend calcula o "melhor dia"
  como o primeiro dia da previsão marcado como `good_for_outdoor`.
- **Filtros e paginação** no backend via `django-filter` e
  `PageNumberPagination` (10 itens por página), mantendo a lógica de
  consulta fora do frontend.
- **Um container por serviço** no `docker-compose.yml` (banco, API externa,
  backend, frontend), refletindo como os serviços rodariam em produção,
  cada um com seu próprio Dockerfile.

## Como rodar

### Com Docker (recomendado)

Pré-requisito: Docker e Docker Compose instalados.

```bash
git clone <url-do-repositorio>
cd todo-list
cp backend/.env.example backend/.env
docker compose up --build
```

Serviços disponíveis:

- Frontend: http://localhost:5173
- Backend (API): http://localhost:8000/api/
- Admin do backend: http://localhost:8000/admin/
- API externa de clima: http://localhost:8001/api/weather/

O `docker-compose.yml` já cuida da ordem de subida (banco → API externa →
backend → frontend) e das variáveis de ambiente do backend via
`backend/.env`.

### Rodando cada serviço manualmente

<details>
<summary>Backend</summary>

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # ajuste DB_HOST=localhost se não usar Docker
python manage.py migrate
python manage.py runserver
```

</details>

<details>
<summary>API externa</summary>

```bash
cd external-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

</details>

<details>
<summary>Frontend</summary>

```bash
cd frontend
npm install
npm run dev
```

</details>

## Testes

| Camada                    | Local           | Comando                            |
| ------------------------- | --------------- | ---------------------------------- |
| Backend (unitários + API) | `backend/`      | `pytest`                           |
| API externa               | `external-api/` | `pytest`                           |
| End-to-end (Selenium)     | `e2e/`          | `pytest -v` (veja `e2e/README.md`) |

O E2E sobe o fluxo completo em um Chrome real: cadastro, login, criação e
conclusão de tarefas. Backend, banco e API externa precisam estar de pé
(via Docker) e o frontend rodando localmente antes de executar.

## CI/CD

O workflow em `.github/workflows/ci.yml` roda a cada push, com três jobs
independentes: testes do backend (pytest), testes da API externa (pytest) e
build do frontend (`npm run build`).

## Status

- [x] Backend (auth JWT, categorias, tarefas, compartilhamento, filtros, paginação, testes pytest)
- [x] API externa de clima + integração com o backend + testes
- [x] Frontend (auth, CRUD de tarefas/categorias, compartilhamento, previsão do tempo, filtros, paginação)
- [x] Docker Compose (banco, API externa, backend, frontend)
- [x] Testes end-to-end (Selenium)
- [x] CI/CD com GitHub Actions
