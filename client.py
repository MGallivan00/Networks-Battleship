
import socket
import sys
# import requests


def fire():

    # format:
    # $python client.py 127.0.0.1 8080  5    7
    #          [0]          [1]   [2]  [3]  [4]

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    xcor = sys.argv[3]
    ycor = sys.argv[4]

    content = "https://" + HOST + ":" + str(PORT) + "?x=" + xcor + "&y=" + ycor

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(content))
        msg = s.recv(1024)
        print('Received:', msg.decode("utf-8"))




fire() # send fire coordinates to server



# receive an answer from server (hit or miss)
# then update opponent own_board
