from zmq import Context, Socket

class Socket:
    def __init__(self, context: Context, protocol: str, ip: str, port: int, socket_type: int):
        self.protocol = protocol
        self.ip = ip
        self.port = port
        self.context = context
        self.socket: Socket = context.socket(socket_type)
        self.socket.connect(f"{protocol}://{ip}:{port}")

    def disconnect(self) -> None:
        pass


