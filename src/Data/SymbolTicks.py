from typing import List
import numpy as np
from datetime import datetime

class SymbolTicks:
    def __init__(self):
        self.bids: List[float] = []
        self.asks: List[float] = []
        # self.volumes = [] # This isn't needed for Forex, since we are going to work out the tick volume
        self.times: List[float] = []
        self.python_times: List[datetime] = []
        self.has_been_processed = True
