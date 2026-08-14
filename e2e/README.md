# Testes E2E (Selenium)

Testes end-to-end que simulam o uso real da aplicação em um navegador
Chrome de verdade, cobrindo o fluxo completo: registro, login, criação
de tarefas, conclusão e logout.

## Pré-requisitos

- Backend, banco de dados e API externa rodando via Docker (`docker compose up -d` na raiz)
- Frontend rodando localmente (`npm run dev` dentro de `frontend/`)
- Google Chrome instalado na máquina

## Como rodar

```powershell
cd e2e
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
```

Por padrão os testes abrem uma janela do Chrome de verdade (não headless),
então você pode acompanhar visualmente. Para rodar sem abrir janela (útil
em CI), descomente a linha `--headless` em `conftest.py`.
