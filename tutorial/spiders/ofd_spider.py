from pathlib import Path
from typing import Iterable

import datetime as dt
import scrapy
from scrapy.http.request import Request

from ..items.CustomMonth import CustomMonth
from ..items.DancerItem import DancerItem
from ..items.DancerScheduleItem import DancerScheduleItem


class OfdScheduleSpider(scrapy.Spider):
    name = "ofd"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'tutorial.middlewares.SeleniumMiddleware': 100
        },
        'ITEM_PIPELINES': {
            'tutorial.pipelines.OFDPipeline': 300,
        },
        'SPIDER_MIDDLEWARES': {
            "tutorial.middlewares.TutorialSpiderMiddleware": 100,
        }
    }

    def __init__(self, *args, **kwargs):
        self.start_urls = [
            "http://onlyfordance.com/schedule",
            "http://onlyfordance.com/schedule"
        ]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method="GET", encoding="utf-8", dont_filter=True)

    def parse(self, response):
        today = dt.date.today()
        currentMonthR: str = response.xpath('//section[@class="date-filter"]/div/span/text()').get()

        if currentMonthR is None:
            return None

        cmTemp = currentMonthR.strip().split()
        currentYear: str = cmTemp[0]
        currentMonth: CustomMonth = CustomMonth.getEnumMonth(month=cmTemp[2])

        calender = response.xpath('//app-calendar[@class="panel ng-star-inserted"]/section')

        weekLessons = calender.xpath('//div[@class="week ng-star-inserted"]')
        for w in weekLessons:
            dayLessons = w.xpath('./div[@class="day ng-star-inserted"]')

            for d in dayLessons:
                enableCheck1 = d.xpath('./div[@class="header"]/p[@class="day enable ng-star-inserted"]').get()
                enableCheck2 = d.xpath('./div[@class="header"]/p[@class="day enable today ng-star-inserted"]').get()
                if enableCheck1 is None and enableCheck2 is None:
                    continue

                dayCount = d.xpath('./div[@class="header"]/p/span/text()').get()
                date = dt.date(year=int(currentYear), month=currentMonth.value[1], day=int(dayCount))

                lessons = d.xpath('./div[@class="body"]/div[@class="item ng-star-inserted"]')

                for l in lessons:
                    startTime = l.xpath('./span[1]/text()').get()
                    temp = startTime.split(":")
                    endTime = str(int(temp[0]) + 1) + ":" + str(int(temp[1]) + 10)
                    name = l.xpath('./span[2]/p[1]/text()').get()
                    classLevel = self._changeClassLevel(len(l.xpath('./span[3]/mat-icon').getall()))

                    dancers = []
                    dancers.append(DancerItem(name=name))
                    dancerScheduleItem = DancerScheduleItem(
                        dancers=dancers,
                        scheduleDate=date.strftime("%Y-%m-%d"),
                        scheduleDay=date.weekday(),
                        startTime=startTime,
                        endTime=endTime,
                        classLevel=classLevel,
                        enterprise="OFD"
                    )

                    if today <= date:
                        yield dancerScheduleItem

    def _changeClassLevel(self, size):
        if size == 1:
            return "Easy"
        elif size == 2:
            return "Medium"
        else:
            return "Hard"
