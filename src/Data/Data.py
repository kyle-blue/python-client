from typing import Dict, List
import threading
from .SymbolTicks import SymbolTicks
from copy import deepcopy

class Data(object):
    """Singleton class with all global raw and derived market data"""
    _lock: threading.Lock = threading.Lock()
    _instance = None
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        if not self.__dict__:
            self.ticks: Dict[str, SymbolTicks] = dict()
            self.min1: Dict[str, List[tuple]] = dict()
            self.lock = Data._lock

    def get_ticks(self):
        self.lock.acquire()
        ticks = deepcopy(self.ticks)
        self.lock.release()
        return ticks


