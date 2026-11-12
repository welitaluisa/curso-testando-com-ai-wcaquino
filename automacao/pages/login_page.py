from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "senha")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Entrar']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, '[role="alert"]')

    def __init__(self, driver: WebDriver, url: str):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 10)

    def open(self) -> None:
        self.driver.get(self.url)

    def login(self, email: str, password: str) -> None:
        self.wait.until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        ).send_keys(email)
        self.wait.until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        ).send_keys(password)
        self.wait.until(
            EC.element_to_be_clickable(self.SUBMIT_BUTTON)
        ).click()

    @property
    def success_message(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.SUCCESS_ALERT)
        ).text

    @property
    def error_message(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.SUCCESS_ALERT)
        ).text