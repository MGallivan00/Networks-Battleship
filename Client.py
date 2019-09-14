import socket
import sys


def fire():
    # coordinates from command line

    HOST = sys.argv[0]
    PORT = sys.argv[1]
    xcor = sys.argv[2]
    ycor = sys.argv[3]

    # split the coordinates
    # add the specific url content

    content = "x=" + xcor + "&y=" + ycor
    print(content)

    requests.post('https://' + HOST + ":" + PORT + "?" + content)

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #   s.connect((HOST, PORT))
    #  s.sendall(b'Ready to play?')
    # data = s.recv(1024)
    # need to send coordinates to server

    return xcor, ycor


print(b'Received', repr(data))

x, y = fire()
