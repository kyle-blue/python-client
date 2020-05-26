import datetime
import threading
from .Data import Data
from copy import copy, deepcopy
import numpy as np
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
            self.process_ticks()

    def process_ticks(self):
        ticks = dict()
        self.data.lock.acquire()
        raw_ticks = deepcopy(self.data.raw_ticks)
        self.data.lock.release()
        for symbol, all_data in raw_ticks.items():
            ticks[symbol] = dict()
            for key, data in all_data.items():
                if type(data) is list and len(data) != 0:
                    if type(data[0]) is int:
                        ticks[symbol][key] = np.array(data, dtype=np.int32)
                    if type(data[0]) is float:
                        ticks[symbol][key] = np.array(data, dtype=np.float64)
                    elif type(data[0]) is datetime.datetime:
                        ticks[symbol][key] = dates.date2num(data)
                    if key not in ticks[symbol]:
                        ticks[symbol][key] = np.array([], dtype=float)
        self.data.ticks = ticks

