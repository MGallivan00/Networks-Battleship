
import socket
import sys



def init():

    if (len(sys.argv) == 1):
        print("Please respect synthax python3 client.py address portnumber xcoordinate ycoordinate.")
        exit()
    if(len(sys.argv) > 1 and len(sys.argv) < 5):
        print("Please enter 4 arguments.")
        exit()
    if(len(sys.argv) > 5):
        print("Please enter only 4 arguments.")
        exit()


def fire():

    # format:
    # $python3 client.py 127.0.0.1 8080  5    7
    #          [0]          [1]   [2]  [3]  [4]

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    xcor = sys.argv[3]
    ycor = sys.argv[4]

    contentlength = 5+len(str(xcor))+len(str(ycor))
    content = "POST \nHost: " + HOST + "\nContent-Type: misc\nContent-Length: " + str(contentlength) + "\n\n" + "x=" + xcor + "&y=" + ycor
    print("\nContent that will be sent:\n" + content)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(content))
        msg = s.recv(1024)
        print('Received:', msg.decode("utf-8"))


init()
fire() # send fire coordinates to server
