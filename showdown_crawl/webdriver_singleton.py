import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


class WebDriver(object):
    driver = None
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WebDriver, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
        WINDOW_SIZE = "1920,1080"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={WINDOW_SIZE}")

        options.add_argument('Content-Type=application/json; charset=utf-8')
        # options.add_argument("--disable-logging")
        # options.add_argument("--log-level=OFF")
        options.binary_location = "/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome"
        # LOGGER.setLevel(logging.WARNING)

        self.driver = webdriver.Chrome(service=ChromeService(executable_path=CHROMEDRIVER_PATH), options=options)
