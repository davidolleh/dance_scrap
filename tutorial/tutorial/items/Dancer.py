import datetime

from scrapy.item import Item
from dataclasses import dataclass


@dataclass
class Dancer:
    name: str
    instargramId: str
    enterprise: str
    crew: str

    def __init__(self, name=None, instargramId=None, enterprise=None, crew=None):
        self.name = name
        self.instargramId = instargramId
        self.enterprise = enterprise
        self.crew = crew
