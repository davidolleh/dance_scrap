from typing import Iterable

import datetime as dt
import scrapy
from scrapy.http.request import Request

from ..items.CustomMonth import CustomMonth
from ..items.DancerItem import DancerItem
from ..items.DancerScheduleItem import DancerScheduleItem


class YGXScheduleSpider(scrapy.Spider):
    name = "ygx"
    result = []
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'showdown_crawl.middlewares.YGXMiddleware': 200
        },
        'ITEM_PIPELINES': {
            'showdown_crawl.pipelines.YGXPipeline': 300,
        },
        'SPIDER_MIDDLEWARES': {
            "showdown_crawl.middlewares.TutorialSpiderMiddleware": 100,
        }
    }

    def __init__(self, *args, **kwargs):
        self.start_urls = [
            "https://www.ygx.co.kr/schedule/calendar.php",
            "https://www.ygx.co.kr/schedule/calendar.php"
        ]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method="GET", encoding="utf-8", dont_filter=True)

    def parse(self, response):
        today = dt.date.today()
        monthResponse: str = response.xpath('//*[@id="sub_contents"]/div/div/div/div/div[1]/em[1]/text()').get()
        currentMonth: CustomMonth = CustomMonth.getEnumMonth(month=monthResponse)

        weekSchedules = response.xpath('//*[@id="sub_contents"]/div/div/div/div/div[3]/table/tbody/tr')
        for weekSchedule in weekSchedules:
            daySchedules = weekSchedule.xpath('.//td')

            for d in daySchedules:
                isPrevClass = d.xpath("@class").get()
                if "prev" in isPrevClass or "disable" in isPrevClass:
                    continue

                # 날짜 얻기
                dayCount = d.xpath('div/em[1]/text()').get().strip()

                lessonsTimes = d.xpath('div/div/div/div[contains(@class, "time_wrap")]')
                for lessonsTime in lessonsTimes:

                    startTimeStr = lessonsTime.xpath('b/text()').get().strip()
                    splitTime = startTimeStr.split(":")
                    startTimeDateTime = dt.datetime(year=2024, month=1, day=1, hour=int(splitTime[0]),
                                                    minute=int(splitTime[1]))
                    endTimeDateTime = startTimeDateTime + dt.timedelta(hours=1, minutes=40)
                    endTimeStr = endTimeDateTime.strftime("%H:%M")

                    lessons = lessonsTime.xpath('div[contains(@class, "class_box")]')
                    for lesson in lessons:
                        classLevel = lesson.xpath("@class").get()
                        if "class01" not in classLevel \
                                and "class02" not in classLevel \
                                and "class07" not in classLevel \
                                and "class08" not in classLevel:
                            continue
                        name = lesson.xpath('p/text()').get().strip()
                        classLevel = lesson.xpath('span/text()').get().strip()

                        date = dt.date(year=2024, month=currentMonth.value[1], day=int(dayCount))

                        dancers = []

                        dancerItem = DancerItem()
                        dancerItem["name"] = name

                        dancers.append(dancerItem)

                        dancerScheduleItem = DancerScheduleItem()
                        dancerScheduleItem["dancers"] = dancers
                        dancerScheduleItem["scheduleDate"] = date.strftime("%Y-%m-%d")
                        dancerScheduleItem["scheduleDay"] = date.weekday()
                        dancerScheduleItem["startTime"] = startTimeStr
                        dancerScheduleItem["endTime"] = endTimeStr
                        dancerScheduleItem["classLevel"] = classLevel
                        dancerScheduleItem["enterprise"] = "YGX"

                        if today <= date:
                            yield dancerScheduleItem

