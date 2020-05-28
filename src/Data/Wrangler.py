from datetime import datetime, timedelta
import threading
from .Data import Data
from typing import List, Tuple
from .SymbolTicks import SymbolTicks
from .Time import Time
from matplotlib import dates


class Wrangler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.data = Data()
        self._stop = threading.Event()
        self.lock = threading.Lock()

    def start(self) -> None:
        self._stop.clear()
        super().start()

    def stop(self) -> None:
        self._stop.set()

    def is_stopped(self) -> bool:
        return self._stop.is_set()

    def run(self) -> None:
        while not self.is_stopped():
            symbols_to_process = []
            self.data.lock.acquire()
            for symbol in self.data.ticks.keys():
                if not self.data.ticks[symbol].has_been_processed:
                    symbols_to_process.append(symbol)
                    self.data.ticks[symbol].has_been_processed = True
            self.data.lock.release()
            for symbol in symbols_to_process:
                self.process(symbol)

    def process(self, symbol: str) -> None:
        self.data.min1[symbol] = self.get_ohlc(self.data.ticks[symbol], (1, Time.MINUTE), using="bid")

    def get_ohlc(self, ticks: SymbolTicks, interval: Tuple[int, Time], *, using: str) -> List[Tuple[float, float, float, float, float, float]]:
        """:return List of tuples. Each tuple contains (time, open, high, low, close, volume)
        :param using: should be either "bid" "ask" or "both" (which means average)
        :param interval: should be a tuple (amount, Time() unit)
        """
        asks = ticks.asks
        bids = ticks.bids
        times = ticks.python_times


        bar_start = self.get_start_bar_time(ticks.python_times[0], interval)
        while True:
            temp = self.add_time(bar_start, interval)
            if temp > ticks.python_times[0]: break
            bar_start = temp

        ohlc = []
        current_tick = 0
        while bar_start < ticks.python_times[-1]:
            next_bar = self.add_time(bar_start, interval)
            start_tick = current_tick
            open = ticks.bids[start_tick]
            volume = 1
            for i in range(current_tick, len(ticks.python_times)):
                if ticks.python_times[i] > next_bar:
                    break
                current_tick = i
                volume += 1
            close = ticks.bids[current_tick]
            try:
                low = min(ticks.bids[start_tick:current_tick])
                high = max(ticks.bids[start_tick:current_tick])
            except:
                low, high = ticks.bids[start_tick], ticks.bids[start_tick]
            ohlc.append((dates.date2num(bar_start), open, high, low, close, volume))
            bar_start = next_bar
        return ohlc





    @staticmethod
    def add_time(time: datetime, interval: tuple):
        new_time = time
        amount, measurement = interval
        if measurement == Time.YEAR:
            new_time = datetime(time.year + amount, time.month, time.day, time.hour, time.minute, time.second)
        if measurement == Time.MONTH:
            new_month = time.month + amount
            new_year = time.year
            if new_month > 12:
                new_month -= 12
                new_year += 1
            new_time = datetime(time.year, time.month + amount, time.day, time.hour, time.minute, time.second)
        if measurement == Time.WEEK:
            new_time = new_time + timedelta(days=amount*7)
        if measurement == Time.DAY:
            new_time = new_time + timedelta(days=amount)
        if measurement == Time.HOUR:
            new_time = new_time + timedelta(hours=amount)
        if measurement == Time.MINUTE:
            new_time = new_time + timedelta(minutes=amount)
        if measurement == Time.SECOND:
            new_time = new_time + timedelta(seconds=amount)

        return new_time

    @staticmethod
    def get_start_bar_time(start_tick: datetime, interval: tuple) -> datetime:
        start = start_tick
        amount, measurement = interval
        if amount > 1:
            measurement = measurement.pred()
        if measurement == Time.YEAR:
            start = datetime(start.year, 1, 1)
        if measurement == Time.MONTH:
            start = datetime(start.year, start.month, 1)
        if measurement == Time.WEEK:
            start = datetime(start.year, start.month, start.day - start.weekday())
        if measurement == Time.DAY:
            start = datetime(start.year, start.month, start.day)
        if measurement == Time.HOUR:
            start = datetime(start.year, start.month, start.day, start.hour)
        if measurement == Time.MINUTE:
            start = datetime(start.year, start.month, start.day, start.hour, start.minute)
        if measurement == Time.SECOND:
            start = datetime(start.year, start.month, start.day, start.hour, start.minute, start.second)
        return start
