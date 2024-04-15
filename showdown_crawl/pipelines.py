# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class YGXPipeline(object):
    def open_spider(self, spider):
        spider.logger.info('Tutorial Spider Pipeline Started')
        # self.file = open("items_19.json", "w")

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        spider.logger.info('Tutorial Spider Pipeline closed')


class OneMillionPipeline(object):

    def open_spider(self, spider):
        spider.logger.info('Tutorial Spider Pipeline Started')

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        spider.logger.info('Tutorial Spider Pipeline closed')

class OFDPipeline(object):

    def open_spider(self, spider):
        spider.logger.info('Tutorial Spider Pipeline Started')

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        spider.logger.info('Tutorial Spider Pipeline closed')