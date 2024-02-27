from typing import Iterable

import datetime as dt
import scrapy
from scrapy.http.request import Request

from ..items.DanceSchedule import DanceSchedule
from ..items.Dancer import Dancer
from ..items.CustomMonth import CustomMonth


class YGXScheduleSpider(scrapy.Spider):
    name = "ygx"
    result = []

    def __init__(self, *args, **kwargs):
        self.start_urls = ["https://www.ygx.co.kr/schedule/calendar.php"]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method="GET", encoding="utf-8")

    def parse(self, response):
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
                    time = lessonsTime.xpath('b/text()').get().strip()
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

                        dancerTemp = Dancer(name=name, enterprise="ygx")
                        date = dt.date(year=2024, month=currentMonth.value[1], day=int(dayCount))
                        danceSchedule = DanceSchedule(
                            dancer=dancerTemp,
                            scheduleDate=date,
                            scheduleDay=date.weekday(),
                            scheduleTime=time,
                            classLevel=classLevel,
                            genre="CHOREOGRAPHER"
                        )

                        self.result.append(danceSchedule)

        print(len(self.result))


