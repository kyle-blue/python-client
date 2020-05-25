import zmq
from typing import Tuple
import re
from .Requester import Requester
from .Subscriber import Subscriber

SERVER_IP, MAIN_PORT = "localhost", 25001

class Client:
    def __init__(self):
        self.context = zmq.Context()
        req_port, sub_port = self.__assign_ports()
        self.requester = Requester(self.context, SERVER_IP, req_port) # TODO: Should requester be a singleton??
        self.subscriber = Subscriber(self.context, SERVER_IP, sub_port)
        self.subscriber.start()

    def __assign_ports(self) -> Tuple[int, int]:
        """
        Makes a request with the MQL server, getting the assigned sub port and req port
        :return (REQ_PORT, SUB_PORT) A tuple with 2 ints. The first int is the
        requester port, the second is the subscriber port"""
        print("Requesting Connection...")
        req_socket = self.context.socket(zmq.REQ)
        req_socket.connect(f"tcp://{SERVER_IP}:{MAIN_PORT}")
        req_socket.send_string("REQUESTING CONNECTION")

        ret = req_socket.recv_string()
        req_socket.disconnect(f"tcp://{SERVER_IP}:{MAIN_PORT}")
        sub_port = re.findall("(?<=SUB_PORT: )[0-9]+(?=\n)", ret)[0]
        req_port = re.findall("(?<=REQ_PORT: )[0-9]+(?=\n)", ret)[0]
        return req_port, sub_port
