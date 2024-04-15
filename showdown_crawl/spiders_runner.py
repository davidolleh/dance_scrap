import datetime as dt
import json

from itemadapter import ItemAdapter
from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from showdown_crawl.spiders.ofd_spider import OfdScheduleSpider
from showdown_crawl.spiders.oneMillion_spider import OneMillionScheduleSpider
from showdown_crawl.spiders.ygx_spider import YGXScheduleSpider

result = []
isExcepted = [False]


def _item_passed(item):
    result.append(item)


def _checkException():
    isExcepted[0] = True


#
settings = get_project_settings()
process = CrawlerProcess(settings)
dispatcher.connect(_item_passed, signals.item_passed)
dispatcher.connect(_checkException, signals.spider_error)

try:
    process.crawl(OneMillionScheduleSpider)
    process.crawl(YGXScheduleSpider)
    process.crawl(OfdScheduleSpider)
    process.start()
except Exception as ex:
    raise Exception()

if isExcepted[0]:
    raise Exception("crawled failed!")

today = str(dt.date.today().day)
file = open("lessons_" + today + ".json", "w")
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
