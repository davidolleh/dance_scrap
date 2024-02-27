from typing import Iterable

import datetime as dt
import scrapy
from scrapy.http.request import Request

from ..items.DanceSchedule import DanceSchedule
from ..items.Dancer import Dancer
from ..items.CustomMonth import CustomMonth


class OneMillionScheduleSpider(scrapy.Spider):
    name = "oneMillion"
    result = []

    def __init__(self, *args, **kwargs):
        self.start_urls = ["https://www.1milliondance.com/schedule"]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method="GET", encoding="utf-8")

    def parse(self, response):
        currentMonthR: str = response.xpath('//*[@id="monthYearHeader_0"]/span/text()').get()

        if currentMonthR is None:
            return None

        cmTemp = currentMonthR.strip().split()
        currentYear: str = cmTemp[1]
        currentMonth: CustomMonth = CustomMonth.getEnumMonth(month=cmTemp[0])

        weekLessons = response.xpath('//*[@id="monthYear_0"]/ul')
        for dayLessons in weekLessons:
            lessons = dayLessons.xpath('./li')
            for index, lesson in enumerate(lessons):
                if index == 0:
                    dayCountR = lesson.xpath('./div[@class="day-count"]/text()').get()
                    dayCount = dayCountR.strip().split()[0]
                    dayTextR = lesson.xpath('./div[@class="day-count"]/text()').get()
                    dayText = dayTextR.strip()

                else:
                    time = lesson.xpath('./div[2]/div/text()').get()
                    name = lesson.xpath('./div[3]/button/text()').get()
                    classLevel = lesson.xpath('./div[4]/div[@class="type"]/span/text()').get()

                    dancerTemp = Dancer(name=name, enterprise="oneMillion")
                    date = dt.date(year=int(currentYear), month=currentMonth.value[1], day=int(dayCount))

                    danceSchedule = DanceSchedule(
                        dancer=dancerTemp,
                        scheduleDate=date,
                        scheduleDay=date.weekday(),
                        scheduleTime=time,
                        classLevel=classLevel,
                    )

                    self.result.append(danceSchedule)