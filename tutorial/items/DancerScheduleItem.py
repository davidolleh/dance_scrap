import datetime

import scrapy

from tutorial.items import DancerItem


class DancerScheduleItem(scrapy.Item):
    dancer = scrapy.Field(serializer=DancerItem)
    scheduleDate = scrapy.Field(serializer=datetime.date)
    scheduleDay = scrapy.Field(serializer=int)
    startTime = scrapy.Field(serializer=str)
    endTime = scrapy.Field(serializer=str)
    classLevel = scrapy.Field(serializer=str)
    genre = scrapy.Field(serializer=str)
