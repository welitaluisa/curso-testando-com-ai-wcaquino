
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        raise RuntimeError(
            f"Variável de ambiente {name} não definida. "
            "Copie .env.example para .env e ajuste os valores antes de executar os testes."
        )
    return value


TEST_LOGIN_URL = os.getenv("TEST_LOGIN_URL", "https://seubarriga.wcaquino.me/")
TEST_LOGIN_EMAIL = _require_env("TEST_LOGIN_EMAIL")
TEST_LOGIN_PASS = _require_env("TEST_LOGIN_PASS")


def test_login_sucesso():

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )

    driver.get(TEST_LOGIN_URL)

    wait = WebDriverWait(driver, 10)

    # Preencher email
    wait.until(
        EC.visibility_of_element_located((By.ID, "email"))
    ).send_keys(TEST_LOGIN_EMAIL)

    # Preencher senha
    wait.until(
        EC.visibility_of_element_located((By.ID, "senha"))
    ).send_keys(TEST_LOGIN_PASS)

    # Clicar em Entrar
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Entrar']")
        )
    ).click()

    # Validar mensagem de sucesso
    alerta = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[role="alert"]')
        )
    )

    assert "Bem vindo" in alerta.text

    print("PASSOU: Login realizado com sucesso!")

    driver.quit()

