from typing import Iterable

import datetime as dt
import scrapy
from scrapy.http.request import Request
from ..items.Dancer import Dancer

class OneMillionDancerSpider(scrapy.Spider):
    name = "oneMillionDancer"
    oneMillionDancers = []


    def __init__(self, *args, **kwargs):
        self.start_urls = [
            "https://www.1milliondance.com/instructors"
        ]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.getDancers, method="GET", encoding="utf-8")

    def getDancers(self, response):
        # //*[@id="root"]/div[2]/div[24]/ul/div[1]/li/a
        dancers = response.xpath('//a[contains(@href, "/instructors/")]/@href').getall()
        nextUrls = []
        index = 0
        for dancer in dancers:
            index += 1
            nextUrls.append("https://www.1milliondance.com" + dancer)
            if index == 2:
                break

        for nextUrl in nextUrls:
            yield scrapy.Request(url=nextUrl, callback=self.getDancerInfo, method="GET", encoding="utf-8")

    def getDancerInfo(self, response):
        info = response.xpath('//span[contains(@class, "info")]')
        name = info.xpath('./div/text()').get()
        instaButton = info.xpath('./ul//li/button')
        crew = response.xpath('//div[contains(@class, "ins-text-box")]/text()').get()
        print("wow1!!")

        print(response.url)
        print(name)
        print(crew)
        print("wow2!!")

        dancer = Dancer(
            name=name,
            # instargramId=
            enterprise="oneMillion",
            crew=crew
        )
        # print(self.driver.find_element_by_xpath('//span[contains(@class, "info")]/ul/li/button'))

        # if len(instaButton) == 1:
        #
        # print(name)

