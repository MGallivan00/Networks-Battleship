import socket
HOST = '127.0.0.1'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Ready to play?')
    data = s.recv(1024)

print(b'Received', repr(data))



def fire():

    # ask for coordinates
    # split the coordinates
    # add the specific url content
    coordinates = input("Choose your next coordinates to bomb: ")
    coordinates = coordinates.split(" ")
    content = "x=" + coordinates[0] + "&y=" + coordinates[1]
    print(content)
    print(type(coordinates[0]))

    # need to send coordinates to server

    return coordinates[0], coordinates[1]