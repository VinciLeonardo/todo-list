import uuid

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

FRONTEND_URL = 'http://localhost:5173'


@pytest.fixture
def driver():
    """Cria uma instância do navegador Chrome para cada teste."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # Remova a linha abaixo se quiser VER o navegador rodando os testes
    # options.add_argument('--headless')
    options.add_argument('--window-size=1280,800')

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)  # espera implícita para elementos aparecerem

    yield driver

    driver.quit()


@pytest.fixture
def unique_user():
    """Gera credenciais únicas para cada execução (evita conflito de usuário duplicado)."""
    suffix = uuid.uuid4().hex[:8]
    return {
        'username': f'e2e_user_{suffix}',
        'email': f'e2e_{suffix}@teste.com',
        'password': 'senha12345',
    }