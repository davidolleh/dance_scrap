from typing import Iterable

import datetime as dt
import scrapy
from scrapy.http.request import Request

from ..items.DancerItem import DancerItem
from ..items.CustomMonth import CustomMonth
from ..items.DancerScheduleItem import DancerScheduleItem


class OneMillionScheduleSpider(scrapy.Spider):
    name = "oneMillion"
    result = []
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'tutorial.middlewares.OneMillionMiddleWare': 100
        },
        'ITEM_PIPELINES': {
           'tutorial.pipelines.OneMillionPipeline': 300,
        }
    }

    def __init__(self, *args, **kwargs):
        self.start_urls = [
            "https://www.1milliondance.com/schedule",
            "https://www.1milliondance.com/schedule"
        ]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method="GET", encoding="utf-8", dont_filter=True)

    def parse(self, response, **kwargs):
        today = dt.date.today()
        monthYearR: str = response.xpath('//*[@class="schdm-month-year"]/text()').get()
        if monthYearR is None:
            return None

        currentYear, currentMonth = self._getMonth(month=monthYearR)

        weeksInfoR = response.xpath('//*[@class="schdm-row"]')
        for weekInfoR in weeksInfoR:
            daysInfoR = weekInfoR.xpath('./div[@class="schdm-col"]')

            for index, dayInfoR in enumerate(daysInfoR):
                countR = dayInfoR.xpath('./div[@class="schdm-col-header"]')
                if len(countR) < 1:
                    continue

                dayCount = dayInfoR.xpath('./div[@class="schdm-col-header"]/text()').get().strip()
                date = dt.date(year=int(currentYear), month=currentMonth.value[1], day=int(dayCount))

                dayLessonsR = dayInfoR.xpath('./div[@class="schdm-col-body"]/div')

                for dayLessonR in dayLessonsR:
                    isCollaboration = False
                    collaborationR = dayLessonR.xpath('./div[2]/text()').get()
                    if collaborationR == 'Collaboration':
                        isCollaboration = True

                    lessonInfoR = dayLessonR.xpath('./div[@class="tooltip"]')
                    time = lessonInfoR.xpath('./div[2]/div/text()').get().strip()
                    startTime, endTime = self._parseOneMillionTime(time=time)

                    name = lessonInfoR.xpath(
                        './div[3]/button/text()'
                    ).get()

                    classLevel = lessonInfoR.xpath(
                        './div[4]/div[@class="type"]/span/text()'
                    ).get()

                    dancers = []

                    if isCollaboration:
                        name = name.splitlines()
                        dancer1 = DancerItem()
                        dancer1["name"] = name[0]
                        dancers.append(dancer1)
                        dancer2 = DancerItem()
                        dancer2["name"] = name[1]
                        dancers.append(dancer2)
                    else:
                        dancerItem = DancerItem()
                        dancerItem["name"] = name
                        dancers.append(dancerItem)

                    dancerScheduleItem = DancerScheduleItem()
                    dancerScheduleItem["dancers"] = dancers
                    dancerScheduleItem["scheduleDate"] = date.strftime("%Y-%m-%d")
                    dancerScheduleItem["scheduleDay"] = date.weekday()
                    dancerScheduleItem["startTime"] = startTime
                    dancerScheduleItem["endTime"] = endTime
                    dancerScheduleItem["classLevel"] = classLevel
                    dancerScheduleItem["enterprise"] = "OneMillion"

                    if today <= date:
                        yield dancerScheduleItem

    def _getMonth(self, month):
        temp = month.split()
        currentYear: str = temp[1]
        currentMonth: CustomMonth = CustomMonth.getEnumMonth(month=temp[0])
        return currentYear, currentMonth

    def _parseOneMillionTime(self, time):
        temp = time.split(' ')
        startTime = temp[0]
        endTime = temp[2]

        if "PM" in temp:
            temp = startTime.split(":")
            startTime = str(int(temp[0]) + 12) + ':' + temp[1]
            temp = endTime.split(":")
            endTime = str(int(temp[0]) + 12) + ':' + temp[1]
        return startTime, endTime
