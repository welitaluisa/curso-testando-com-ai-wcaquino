
import subprocess

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage

LOGIN_URL = "https://seubarriga.wcaquino.me/"
EMAIL = "a@a"
SENHA = "a"
INVALID_EMAIL = "usuario.inexistente@example.com"
INVALID_PASSWORD = "senha_incorreta"
LOGIN_ERROR_MESSAGE = "Problemas com o login do usuário"


@pytest.fixture
def driver():
    browser = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install(),
            log_output=subprocess.DEVNULL,
        )
    )
    try:
        yield browser
    finally:
        browser.quit()


def test_login_sucesso(driver):
    login_page = LoginPage(driver, LOGIN_URL)

    login_page.open()
    login_page.login(EMAIL, SENHA)

    assert "Bem vindo" in login_page.success_message


def test_login_credenciais_invalidas(driver):
    login_page = LoginPage(driver, LOGIN_URL)

    login_page.open()
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)

    assert LOGIN_ERROR_MESSAGE in login_page.error_message

