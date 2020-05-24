import zmq
import re
import time


def main():
    context = zmq.Context()
    ip, port = "localhost", 5555

    print("Requesting Connection...")
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{ip}:{port}")
    socket.send_string("REQUESTING CONNECTION")

    ret = socket.recv_string()
    socket.disconnect(f"tcp://{ip}:{port}")
    port = int(re.findall("[0-9]+$", ret)[0])
    socket.connect(f"tcp://{ip}:{port}")
    print(f"Connected to {ip} on port {port}")

    print("Disconnecting")
    socket.send_string("REMOVE CONNECTION")
    ret = socket.recv_string()
    if ret == "OK":
        socket.disconnect(f"tcp://{ip}:{port}")

    # msg = socket.recv_string()
    # print(msg)


if __name__ == "__main__":
    main()