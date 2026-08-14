from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FRONTEND_URL = 'http://localhost:5173'


def test_user_can_register_login_create_task_and_logout(driver, unique_user):
    wait = WebDriverWait(driver, 10)

    # 1. Registro
    driver.get(f'{FRONTEND_URL}/register')

    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys(unique_user['username'])
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(unique_user['email'])
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys(unique_user['password'])
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # 2. Deve redirecionar automaticamente para /tasks, já autenticado
    wait.until(EC.url_contains('/tasks'))
    assert '/tasks' in driver.current_url

    # 3. Criar uma tarefa
    task_title = 'Tarefa criada via Selenium'
    title_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Nova tarefa...']"))
    )
    title_input.send_keys(task_title)
    driver.find_element(By.XPATH, "//form[contains(@class,'task-form')]//button[@type='submit']").click()

    # 4. Confirmar que a tarefa aparece na lista
    task_item = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//li[contains(., '{task_title}')]"))
    )
    assert task_title in task_item.text

# 5. Marcar como concluída
    task_xpath = f"//li[contains(., '{task_title}')]"
    checkbox = driver.find_element(By.XPATH, f"{task_xpath}//input[@type='checkbox']")
    checkbox.click()

    def task_is_marked_completed(d):
        try:
            element = d.find_element(By.XPATH, task_xpath)
            return 'completed' in element.get_attribute('class')
        except Exception:
            return False

    wait.until(task_is_marked_completed)

    # 6. Logout
    driver.find_element(By.XPATH, "//button[text()='Sair']").click()
    wait.until(EC.url_contains('/login'))
    assert '/login' in driver.current_url


def test_login_with_invalid_credentials_shows_error(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(f'{FRONTEND_URL}/login')

    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys('usuario_que_nao_existe')
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys('senha_errada')
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    error_message = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'error-message'))
    )
    assert 'inválid' in error_message.text.lower()