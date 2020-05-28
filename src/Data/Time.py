from enum import Enum, auto


class Time(Enum):
    YEAR = 0
    MONTH = 1
    WEEK = 2
    DAY = 3
    HOUR = 4
    MINUTE = 5
    SECOND = 6

    def pred(self):
        v = self.value - 1
        if v == -1:
            v = 0
        return Time(v)
