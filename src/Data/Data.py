from typing import Any
import threading


class Data(object):
    """Singleton class with all global raw and derived market data"""
    _lock: threading.Lock = threading.Lock()
    _instance = None
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        if not self.__dict__:
            self.raw_ticks = dict()
            self.ticks = dict()
            self.lock = Data._lock

