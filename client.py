
import socket
import sys


def fire():

    # format:
    # $python3 client.py 127.0.0.1 8080  5    7
    #          [0]          [1]   [2]  [3]  [4]

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    xcor = sys.argv[3]
    ycor = sys.argv[4]

    post_format = """   POST /test HTTP/1.1
                        Host: 127.0.0.1
                        Content-Type: application/x-www-form-urlencoded
                        Content-Length: 27

                        field1=value1&field2=value2 """

    contentlength = 5+int(len(str(xcor)))+int(len(str(ycor)))
    content = "POST \nHost: " + HOST + "\nContent-Type: \nContent-Length: " + str(contentlength) + "\n\n" + "x=" + xcor + "&y=" + ycor
    print(content)
    # content = "https://" + HOST + ":" + str(PORT) + "?x=" + xcor + "&y=" + ycor

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(content))
        msg = s.recv(1024)
        print('Received:', msg.decode("utf-8"))

        # update oponent board and my board


fire() # send fire coordinates to server
