import os, subprocess, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.remote_connection import LOGGER
import time

# Dados de login (usuário válido já cadastrado)
EMAIL = "a@a"
SENHA = "a"

LOGGER.setLevel(logging.WARNING)
os.environ["WDM_LOG_LEVEL"] = "0"  # reduzir logs do webdriver-manager

opts = Options()
# Evita "DevTools listening..." e outros
opts.add_experimental_option("excludeSwitches", ["enable-logging"])
# Diminui nível de log do Chrome (0=INFO, 3=ERROR)
opts.add_argument("--log-level=3")
# (se rodar headless) opts.add_argument("--headless=new")

# Redireciona o log do ChromeDriver para /dev/null (ou PIPE)
service = Service(
    ChromeDriverManager().install(),
    log_output=subprocess.DEVNULL  # no Windows funciona também
)

driver = webdriver.Chrome(service=service, options=opts)

try:
    # 1. Acessar a página de login
    driver.get("https://seubarriga.wcaquino.me/")
    # driver.maximize_window()

    # 2. Preencher o campo "Email"
    # email_input = driver.find_element(By.ID, "email-errado")
    email_input = driver.find_element(By.ID, "email")
    email_input.clear()
    email_input.send_keys(EMAIL)

    # 3. Preencher o campo "Senha"
    senha_input = driver.find_element(By.ID, "senha")
    senha_input.clear()
    senha_input.send_keys(SENHA)

    # 4. Clicar no botão "Entrar"
    entrar_button = driver.find_element(By.XPATH, "//button[text()='Entrar']")
    entrar_button.click()

    # 5. Verificar o resultado esperado
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-success']"))
    )

    mensagem = driver.find_element(By.XPATH, "//div[@class='alert alert-success']").text
    print("✅ Login realizado com sucesso! Mensagem exibida:", mensagem)

    time.sleep(3)

except Exception as e:
    print("❌ Erro durante a execução do teste:", str(e))

finally:
    driver.quit()
