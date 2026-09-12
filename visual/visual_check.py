from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from applitools.selenium import Eyes, Target, BatchInfo
from applitools.common import MatchLevel

API_KEY = "rm99S6RE3wFzPYQAIHDbiTG7KHmBFAE6O6xuxbcuREvs110" # Sua chave aqui!
BASE_DIR = Path(__file__).resolve().parent

def file_url(name: str) -> str:
    return (BASE_DIR / name).resolve().as_uri()

def new_driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1200,800")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

def run_check(page_name: str, match: MatchLevel = MatchLevel.STRICT):
    driver = new_driver()
    eyes = Eyes()
    eyes.api_key = API_KEY
    eyes.batch = BatchInfo(f"Visual Tests-Store ({match.name})")

    try:
        eyes.open(driver, "Store", f"CheckHome({match.name})", {"width":1200, "height":800})
        driver.get(file_url(page_name))

        t = Target.window().fully()

        if match == MatchLevel.LAYOUT:
            t = t.layout()
        
        eyes.check("Página inteira", t)
        eyes.close_async()
    finally:
        driver.quit()
        eyes.abort_async()

if __name__ == "__main__":
    # 1) Selecione o level desejado (STRICT ou LAYOUT)
    level = MatchLevel.STRICT
    # level = MatchLevel.LAYOUT


    # 2) Rode em v1.html para gerar baseline
    run_check("html/v1.html", level)
    
    # 3) Rode em v2.html para comparar e observar resultados
    run_check("html/v2.html", level)
    