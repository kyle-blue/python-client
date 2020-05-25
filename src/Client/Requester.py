from .Socket import Socket as ClientSocket
from zmq import Context
import zmq


class Requester(ClientSocket):
    def __init__(self, context: Context, ip: str, port: int):
        super().__init__(context, "tcp", ip, port, zmq.REQ)
        print(f"Requester connected to {self.ip} on port {self.port}")

    def disconnect(self) -> None:
        print("Disconnecting REQ_SOCKET")
        self.socket.send_string("REMOVE CONNECTION")
        ret = self.socket.recv_string()
        if ret == "OK":
            self.socket.disconnect(f"tcp://{self.ip}:{self.port}")