import datetime

from dataclasses import dataclass
from ..items.Dancer import Dancer


@dataclass
class DanceSchedule:
    dancer: Dancer
    scheduleDate: datetime.date
    scheduleDay: int
    scheduleTime: str
    classLevel: str
    genre: str

    def __init__(self, dancer=None, scheduleDate=None, scheduleDay=None, scheduleTime=None, classLevel=None, genre=None):
        self.dancer = dancer
        self.scheduleDate = scheduleDate
        self.scheduleDay = scheduleDay
        self.scheduleTime = scheduleTime
        self.classLevel = classLevel
        self.genre = genre

