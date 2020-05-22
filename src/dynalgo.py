import zmq


def main():
    context = zmq.Context()

    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    for i in range(10):
        print(f"Sending request: {i}")
        socket.send_string(f"Hello number {i}")

        message = socket.recv_string()
        print(f"Reply: {message}")

if __name__ == "__main__":
    main()