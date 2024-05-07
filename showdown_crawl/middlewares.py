# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time
from time import sleep

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from webdriver_singleton import WebDriver
import logging

class YGXMiddleware(object):
    url = []

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        self.driver = WebDriver().driver
        self.wait = WebDriverWait(self.driver, timeout=120)
        self.logger = logging.getLogger()

        spider.logger.info("Spider opened: %s" % spider.name)

    def spider_closed(self, spider):
        self.driver.close()

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        return response

    def process_request(self, request, spider):
        if "robots.txt" in request.url:
            self.logger.warning(request.url)
            return

        self.logger.warning("request!: %s" % request.url)
        self.driver.get(request.url)
        self.logger.warning("request done: %s" % request.url)


        self.logger.warning("waiting for element loaded %s" % request.url)
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="sub_contents"]/div/div/div/div/div[3]/table/tbody'))
        )
        self.logger.warning("success element loaded %s" % request.url)

        if request.url in self.url:
            nextB = self.driver.find_element(By.XPATH, '//a[@class="next"]')
            nextB.click()
            self.logger.warning("waiting for next element loaded %s" % request.url)
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="sub_contents"]/div/div/div/div/div[3]/table/tbody'))
            )
            self.logger.warning("success next element loaded %s" % request.url)
            body = to_bytes(text=self.driver.page_source)
        else:
            self.url.append(request.url)
            body = to_bytes(text=self.driver.page_source)

        response = HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

        return response

class OFDMiddleware(object):
    url = []
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        self.driver = WebDriver(False).driver
        self.wait = WebDriverWait(self.driver, timeout=300)
        self.logger = logging.getLogger()
        spider.logger.info("Spider opened: %s" % spider.name)

    def spider_closed(self, spider):
        self.driver.close()

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        return response

    def process_request(self, request, spider):
        if "robots.txt" in request.url:
            return

        self.logger.warning("request!: %s" % request.url)
        self.driver.get(request.url)
        self.logger.warning("request done!: %s" % request.url)

        # time.sleep(3)
        try:
            self.logger.warning("waiting for info")
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-page-fill-frame/div/bigsoft-menu/mat-sidenav-container/mat-sidenav-content/app-schedule/section[3]/app-calendar/section/div[1]'))
            )
            self.logger.warning("success to load info")
        except Exception as ex:
            self.logger.warning(ex)


        if request.url in self.url:
            nextB = self.driver.find_element(By.XPATH, '//button[@class="mat-focus-indicator mat-icon-button mat-button-base"]')
            nextB.click()
            sleep(2)
            body = to_bytes(text=self.driver.page_source)
        else:
            self.url.append(request.url)
            body = to_bytes(text=self.driver.page_source)

        response = HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

        return response


class OneMillionMiddleWare(object):
    url = []
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        # 언제 이 함수가 작동되는 지 알기 매 request마다 아니면 spider를 실행할 때 한번?
        self.driver = WebDriver(True).driver
        self.wait = WebDriverWait(self.driver, timeout=120)
        self.logger = logging.getLogger()

        spider.logger.info("Spider opened: %s" % spider.name)

    def spider_closed(self, spider):
        self.driver.close()

    def process_response(self, request, response, spider):
        return response

    def process_request(self, request, spider):

        if "robots.txt" in request.url:
            return

        self.driver.execute_script("""
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = 'body { visibility: hidden !important; }';
            document.head.appendChild(style);
        """)
        try:
            self.logger.warning("request!: %s" % request.url)
            self.driver.get(request.url)
            self.logger.warning("request done!: %s" % request.url)
        except Exception as ex:
            self.logger.warning(ex)
            raise ex

        if "1milliondance.com/schedule" in request.url:
            try:
                self.logger.warning("waiting for info")
                self.wait.until(
                    # EC.presence_of_element_located((By.XPATH, '//*[@id="monthYear_0"]/ul[2]/li[2]/div[2]/div'))
                    EC.presence_of_element_located((By.XPATH, '//*[@id="monthYear_0"]/ul[2]'))
                )
                self.logger.warning("success to load info")
            except Exception as ex:
                self.logger.warning(ex)
                raise ex

        if request.url in self.url:
            monthB = self.driver.find_element(By.XPATH, '//button[@class="schdc-monthview "]')
            monthB.click()
            try:
                self.logger.warning("wait for changing to monthview2")
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="schedule-top"]/div[3]/div[4]/div/div[2]/div[2]/div[1]/div[1]'))
                )
                self.logger.warning("success to changed to monthview2")
            except Exception as ex:
                self.logger.warning(ex)
            nextB = self.driver.find_element(By.XPATH, '//button[@class="schda-next"]')
            nextB.click()
            # TODO:: 만약에 정보가 없을때 어떻게 할지 고민해보기 계속해서 기다리게 할 수 없음
            try:
                self.logger.warning("waiting for next info")
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="schedule-top"]/div[3]/div[4]/div/div[7]/div[1]'))
                )
                self.logger.warning("success to load for next info")
            except Exception as ex:
                self.logger.warning(ex)
            body = to_bytes(text=self.driver.page_source)
        else:
            self.url.append(request.url)

            monthB = self.driver.find_element(By.XPATH, '//button[@class="schdc-monthview "]')
            monthB.click()
            try:
                self.logger.warning("wait for changing to monthview1")
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="schedule-top"]/div[3]/div[4]/div/div[2]/div[2]/div[1]/div[1]'))
                )
                self.logger.warning("success to changed to monthview1")
            except Exception as ex:
                self.logger.warning(ex)

            body = to_bytes(text=self.driver.page_source)

        response = HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

        return response


class TutorialSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        raise Exception("business error")

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)