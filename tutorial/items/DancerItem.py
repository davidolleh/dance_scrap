import scrapy


class DancerItem(scrapy.Item):
    name = scrapy.Field(serializer=str)
    instagramId = scrapy.Field(serializer=str)
    enterprise = scrapy.Field(serializer=str)
    crew = scrapy.Field(serializer=str)
