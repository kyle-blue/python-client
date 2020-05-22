import zmq
import time

context = zmq.Context.instance()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv_string()
    print(f"Recieved request: {message}")

    # time.sleep(1)

    socket.send_string("Ur dumb")