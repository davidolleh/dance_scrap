import datetime as dt
import json

from itemadapter import ItemAdapter
from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from tutorial.spiders.oneMillion_spider import OneMillionScheduleSpider
from tutorial.spiders.ygx_spider import YGXScheduleSpider

result = []


def _item_passed(item):
    result.append(item)


#
settings = get_project_settings()
process = CrawlerProcess(settings)
dispatcher.connect(_item_passed, signals.item_passed)

process.crawl(OneMillionScheduleSpider)
process.crawl(YGXScheduleSpider)

process.start()

today = str(dt.date.today().day)
file = open("items_" + today + ".json", "w")
file.write("[" + "\n")
size = len(result) - 1
for index, item in enumerate(result):
    if index == size:
        line = json.dumps(ItemAdapter(item).asdict())
        file.write(line)
    else:
        line = json.dumps(ItemAdapter(item).asdict()) + ",\n"
        file.write(line)

file.write("]")

