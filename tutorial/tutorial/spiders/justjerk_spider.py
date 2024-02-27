from pathlib import Path
from typing import Iterable

import scrapy
from scrapy.http.request import Request


class JustJerkScheduleSpider(scrapy.Spider):
    name = "justjerk"

    def __init__(self, *args, **kwargs):
        self.start_urls = ["https://jerkdemy.com/16"]

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method="GET", encoding="utf-8")

    def parse(self, response):
        filename = f" {self.name}_schedule.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
