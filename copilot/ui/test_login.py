import logging
import os
import subprocess

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


LOGIN_URL = os.getenv("TEST_LOGIN_URL", "https://seubarriga.wcaquino.me/")
EMAIL = os.getenv("TEST_LOGIN_EMAIL", "a@a")
SENHA = os.getenv("TEST_LOGIN_PASS", "a")

LOGGER.setLevel(logging.WARNING)
os.environ["WDM_LOG_LEVEL"] = "0"


@pytest.fixture
def driver():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")

    browser = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install(),
            log_output=subprocess.DEVNULL,
        ),
        options=options,
    )
    try:
        yield browser
    finally:
        browser.quit()


def test_login_sucesso(driver):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(EMAIL)
    wait.until(EC.visibility_of_element_located((By.ID, "senha"))).send_keys(SENHA)
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Entrar']"))
    ).click()

    alerta = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.alert.alert-success")
        )
    )

    assert alerta.text.strip(), "A mensagem de sucesso do login está vazia"