import datetime

import scrapy

from showdown_crawl.items import DancerItem


class DancerScheduleItem(scrapy.Item):
    dancers = scrapy.Field(serializer=list[DancerItem])
    scheduleDate = scrapy.Field(serializer=datetime.date)
    scheduleDay = scrapy.Field(serializer=int)
    startTime = scrapy.Field(serializer=str)
    endTime = scrapy.Field(serializer=str)
    classLevel = scrapy.Field(serializer=str)
    genre = scrapy.Field(serializer=str)
    enterprise = scrapy.Field(serializer=str)
