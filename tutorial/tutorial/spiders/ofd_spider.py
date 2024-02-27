from pathlib import Path
from typing import Iterable

import datetime as dt
import scrapy
from scrapy.http.request import Request

# from ..items.DanceSchedule import DanceSchedule
# from ..items.Dancer import Dancer
from ..items.CustomMonth import CustomMonth


class OfdScheduleSpider(scrapy.Spider):
    name = "ofd"
    result = []

    def __init__(self, *args, **kwargs):
        self.start_urls = ["http://onlyfordance.com/schedule"]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method="GET", encoding="utf-8")

    def parse(self, response):
        currentMonthR: str = response.xpath('//section[@class="date-filter"]/div/span/text()').get()

        if currentMonthR is None:
            return None

        cmTemp = currentMonthR.strip().split()
        currentYear: str = cmTemp[0]
        currentMonth: CustomMonth = CustomMonth.getEnumMonth(month=cmTemp[2])
        print(currentYear)
        print(currentMonth)
        print("yes!")

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

                # for l in lessons:

