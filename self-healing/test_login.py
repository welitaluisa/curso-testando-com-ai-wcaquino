import os
import time
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


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


def new_driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1200,800")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)


def new_remote_driver():
    NODE_URL = "http://localhost:8085"  # Healenium proxy

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1200,800")
    return webdriver.Remote(command_executor=NODE_URL, options=opts)


def _login_flow(driver, page_url: str):
    driver.get(page_url)

    email = driver.find_element(By.ID, "email")
    pwd = driver.find_element(By.ID, "senha")
    btn = driver.find_element(By.XPATH, "//button[@type='submit']")

    email.send_keys(TEST_LOGIN_EMAIL)
    pwd.send_keys(TEST_LOGIN_PASS)
    btn.click()

    time.sleep(1)
    timestamp = int(time.time())
    screenshot_path = BASE_DIR / "images" / f"screenshot_{timestamp}.png"
    driver.save_screenshot(str(screenshot_path))

    msg_text = driver.find_element(By.CSS_SELECTOR, "div.alert.alert-success").text
    assert "Bem vindo" in msg_text


def test_login():
    barriga_url = TEST_LOGIN_URL
    # barriga_url = "https://barrigareact.wcaquino.me"

    # driver = new_driver() #Regular driver
    driver = new_remote_driver()  # Healenium driver

    try:
        _login_flow(driver, barriga_url)
    finally:
        driver.quit()