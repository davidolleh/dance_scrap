from typing import Iterable

import datetime as dt
import scrapy
from scrapy.http.request import Request
import pandas as pd

from ..items.DanceSchedule import DanceSchedule
from ..items.Dancer import Dancer
from ..items.CustomMonth import CustomMonth


class DanceScheduleSpider(scrapy.Spider):
    name = "all"
    result = []
    index = 0

    def __init__(self, *args, **kwargs):
        self.start_urls = [
            "https://www.1milliondance.com/schedule",
            "https://www.ygx.co.kr/schedule/calendar.php",
            "https://www.ygx.co.kr/schedule/calendar.php"
        ]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method="GET", encoding="utf-8", dont_filter=True)

    def parse(self, response):

        if "1million" in response.url:
            self.oneMillionS(response=response)
        elif "ygx" in response.url:
            self.ygxC(response=response)

        self.index += 1

        if self.index == len(self.start_urls):
            self.writeExcel()

    def oneMillionS(self, response):
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

        nextMonth: str = response.xpath('//*[@id="monthYearHeader_1"]/span/text()').get()

        if nextMonth is None:
            return None

        cmTemp = currentMonthR.strip().split()
        currentYear: str = cmTemp[1]
        currentMonth: CustomMonth = CustomMonth.getEnumMonth(month=cmTemp[0])

        weekLessons = response.xpath('//*[@id="monthYear_1"]/ul')
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

    def ygxC(self, response):
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

    def writeExcel(self):
        data = pd.DataFrame(
            [
                (s.scheduleDate,
                 s.scheduleDay,
                 s.scheduleTime,
                 s.dancer.name,
                 s.dancer.instargramId,
                 s.dancer.enterprise,
                 s.dancer.crew,
                 s.classLevel,
                 s.genre
                 ) for s in self.result
            ],
            columns=
            [
                '수업_날짜',
                '수업_요일',
                '수업_시간',
                '댄서_이름',
                '댄서_인스타그램_아이디',
                '댄서_회사',
                '댄서_크루',
                '수업_난이도',
                '수업_장르'
            ],
        )
        print(data)
