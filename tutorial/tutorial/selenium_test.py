from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

CHROMEDRIVER_PATH = "C:/Users/asher/.wdm/drivers/chromedriver/win64/121.0.6167.85/chromedriver-win32/chromedriver.exe"
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")  # 크롬창이 열리지 않음
chrome_options.add_argument("--no-sandbox")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
chrome_options.add_argument("--disable-gpu")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
chrome_options.add_argument('Content-Type=application/json; charset=utf-8')

driver = webdriver.Chrome(service=ChromeService(executable_path=CHROMEDRIVER_PATH), options=chrome_options)
driver.get("https://news.naver.com")
