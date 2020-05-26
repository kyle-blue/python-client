import json
from datetime import datetime
from json.decoder import JSONDecodeError

from .Socket import Socket as ClientSocket
from zmq import Context
import zmq
import threading
from ..Data import Data


class Subscriber(ClientSocket, threading.Thread):
    def __init__(self, context: Context, ip: str, port: int):
        ClientSocket.__init__(self, context, "tcp", ip, port, zmq.SUB)
        threading.Thread.__init__(self)
        self.data = Data()
        self._stop = threading.Event()
        self.socket.subscribe("")
        print(f"Subscriber connected to {self.ip} on port {self.port}")

    def disconnect(self) -> None:
        self.socket.disconnect(f"tcp://{self.ip}:{self.port}")

    def stop(self) -> None:
        self.disconnect()
        self._stop.set()

    def start(self) -> None:
        self._stop.clear()
        super().start()

    def stopped(self):
        return self._stop.isSet()

    def run(self) -> None:
        raw_ticks = self.data.raw_ticks
        while not self.stopped():
            try:
                json_info = json.loads(self.socket.recv_string())
            except JSONDecodeError as e:
                continue  # This means no updates occurred

            if json_info["type"] != "MARKET_INFO":
                continue
            for info in json_info["symbols"]:
                symbol = info["symbol"]
                self.data.lock.acquire()
                if symbol not in raw_ticks:
                    raw_ticks[symbol] = {"bids": [], "asks": [], "volumes": [], "times": []}
                raw_ticks[symbol]["bids"].append(info["bid"])
                raw_ticks[symbol]["asks"].append(info["ask"])
                raw_ticks[symbol]["volumes"].append(info["volume"])
                raw_ticks[symbol]["times"].append(datetime.strptime(info["time"], "%Y.%m.%d %H:%M:%S"))
                self.data.lock.release()

