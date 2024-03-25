# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time
from time import sleep

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class OneMillionDancerDownloaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 크롬창이 열리지 않음
        chrome_options.add_argument("--no-sandbox")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
        chrome_options.add_argument("--disable-gpu")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
        chrome_options.add_argument('Content-Type=application/json; charset=utf-8')

        driver = webdriver.Chrome(service=ChromeService(executable_path=CHROMEDRIVER_PATH), options=chrome_options)
        driver.implicitly_wait(time_to_wait=10)
        self.driver = driver

        self.wait = WebDriverWait(self.driver, 5)
        spider.logger.info("Spider opened: %s" % spider.name)

    def spider_closed(self, spider):
        self.driver.close()

    def process_response(self, request, response, spider):
        return response

    def process_request(self, request, spider):
        spider.logger.info("request!: %s" % request.url)
        self.driver.get(request.url)
        sleep(3)
        self.driver.implicitly_wait(time_to_wait=20)
        instaUrl = None
        if '/instructors/' in request.url:
            instaUrl = self.findInstaButton()
            self.driver.switch_to.window(self.driver.window_handles[0])

        body = to_bytes(text=self.driver.page_source)

        # response = HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)
        response = SubHtmlResponse(url=request.url, body=body, encoding='utf-8', request=request, insta=instaUrl)

        return response

    def findInstaButton(self):
        instaButton = self.driver.find_elements(By.XPATH, '//span[@class="info"]//button[@class="instagram"]')
        if len(instaButton) == 1:
            instaButton[0].click()
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            instaUrl = self.driver.current_url
            return instaUrl





class SeleniumMiddleware(object):
    url = []
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 크롬창이 열리지 않음
        chrome_options.add_argument("--no-sandbox")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
        chrome_options.add_argument("--disable-gpu")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
        chrome_options.add_argument('Content-Type=application/json; charset=utf-8')

        driver = webdriver.Chrome(service=ChromeService(executable_path=CHROMEDRIVER_PATH), options=chrome_options)
        driver.implicitly_wait(time_to_wait=10)
        self.driver = driver

        self.wait = WebDriverWait(self.driver, 5)
        spider.logger.info("Spider opened: %s" % spider.name)

    def spider_closed(self, spider):
        self.driver.close()

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        return response

    def process_request(self, request, spider):
        spider.logger.info("request!: %s" % request.url)
        wait = WebDriverWait(self.driver, 10)
        self.driver.implicitly_wait(time_to_wait=20)
        self.driver.get(request.url)
        sleep(3)


        if request.url in self.url:
            if "ygx" in request.url:
                nextB = self.driver.find_element(By.XPATH, '//a[@class="next"]')
                nextB.click()
                sleep(2)
                body = to_bytes(text=self.driver.page_source)
            else:
                nextB = self.driver.find_element(By.XPATH, '//button[@class="mat-focus-indicator mat-icon-button mat-button-base"]')
                nextB.click()
                sleep(2)
                body = to_bytes(text=self.driver.page_source)

        else:
            self.url.append(request.url)

            if "1million" in request.url and "schedule" in request.url:
                monthB = self.driver.find_element(By.XPATH, '//button[@class="schdc-monthview "]')
                monthB.click()
                sleep(2)
                body = to_bytes(text=self.driver.page_source)
            else:
                body = to_bytes(text=self.driver.page_source)

        response = HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

        return response


class OneMillionMiddleWare(object):
    url = []
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 크롬창이 열리지 않음
        chrome_options.add_argument("--no-sandbox")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
        chrome_options.add_argument("--disable-gpu")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
        chrome_options.add_argument('Content-Type=application/json; charset=utf-8')

        driver = webdriver.Chrome(service=ChromeService(executable_path=CHROMEDRIVER_PATH), options=chrome_options)
        driver.implicitly_wait(time_to_wait=10)
        self.driver = driver

        self.wait = WebDriverWait(self.driver, 5)
        spider.logger.info("Spider opened: %s" % spider.name)

    def spider_closed(self, spider):
        self.driver.close()

    def process_response(self, request, response, spider):
        return response

    def process_request(self, request, spider):
        spider.logger.info("request!: %s" % request.url)
        wait = WebDriverWait(self.driver, timeout=10)
        # self.driver.implicitly_wait(time_to_wait=20)
        self.driver.get(request.url)
        if "1milliondance.com/schedule" in request.url:
            print('wait!!')
            wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="monthYear_0"]/ul[3]/li[2]'))
            )
            print('wait finished!!')
        # sleep(3)

        if request.url in self.url:
            if "1milliondance.com/schedule" in request.url:
                monthB = self.driver.find_element(By.XPATH, '//button[@class="schdc-monthview "]')
                monthB.click()
                sleep(2)
                nextB = self.driver.find_element(By.XPATH, '//button[@class="schda-next"]')
                nextB.click()
                sleep(2)
                body = to_bytes(text=self.driver.page_source)
            else: # robot.txt 걸러 내기?
                body = to_bytes(text=self.driver.page_source)
        else:
            self.url.append(request.url)
            if "1milliondance.com/schedule" in request.url:
                monthB = self.driver.find_element(By.XPATH, '//button[@class="schdc-monthview "]')
                monthB.click()
                # sleep(2)
                body = to_bytes(text=self.driver.page_source)
            else: # robot.txt 걸러 내기?
                body = to_bytes(text=self.driver.page_source)

        response = HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

        return response


class TutorialSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SubHtmlResponse(HtmlResponse):
    insta:str

    def __init__(self, insta, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.insta=insta
