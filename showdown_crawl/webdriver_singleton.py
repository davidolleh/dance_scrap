import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


class WebDriver(object):
    def __init__(self, proxy):
        CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
        WINDOW_SIZE = "1920,1080"

        options = webdriver.ChromeOptions()
        # gui 없이 크롤링 하기
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")

        options.add_argument('--incognito')
        options.add_argument('--disable-blink-features=AutomationControlled')

        # window size 일정하게 유지
        options.add_argument(f"--window-size={WINDOW_SIZE}")

        # 속도 개선을 위한 이미 파일들 안가져오기 이거 ONEMILLION 때문에 사용 하지 말자
        # options.add_argument('--disable-images')
        # options.add_experimental_option(
        #     "prefs", {
        #         # blocked images
        #         'profile.managed_default_content_settings.images': 2,
        #         # "profile.default_content_setting_values.javascript": 2
        #     }
        # )
        # options.add_argument('--blink-settings=imagesEnabled=false')

        user_agent = f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        options.add_argument(user_agent)

        options.add_argument('Content-Type=application/json; charset=utf-8')

        # mac os 전용
        options.binary_location = "/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome"
        # LOGGER.setLevel(logging.WARNING)
        # options.add_argument("--disable-logging")
        # options.add_argument("--log-level=OFF")

        # tor proxy
        if proxy:
            PROXY = "127.0.0.1:9080"
            options.add_argument('--proxy-server=%s' % PROXY)

        self.driver = webdriver.Chrome(service=ChromeService(executable_path=CHROMEDRIVER_PATH), options=options)
