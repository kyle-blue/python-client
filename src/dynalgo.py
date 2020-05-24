import zmq
import re


def main():
    context = zmq.Context()
    ip, port = "localhost", 5555

    print("Requesting Connection...")
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{ip}:{port}")
    socket.send_string("Requesting Connection")
    port = int(re.findall("[0-9]+$", str(socket.recv_string()))[0])
    socket.close()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{ip}:{port}")
    print(f"Connected to {ip} on port {port}")

    msg = socket.recv_string()
    print(msg)


if __name__ == "__main__":
    main()