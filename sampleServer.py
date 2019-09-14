import socket
import os


print("BattleShip game\n")
F = open("own_board.txt","r");
text = F.readlines()
print("Here is your board");
for x in text:
    print(x)




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket
s.bind (("127.0.0.1", 8080)) # bind the socket with IP address and port number
s.listen(1) # accepts one error before crashing. listens for connection
while 1:
    # connection is the connection between the two entities
    # address is the address bound to the socket on the other side of the connection
    connection, address = s.accept()
    data = connection.recv(99999) # the max byte size that the connection can receive

    # decodes the bytes and splits the first byte (4 bits)
    # that is the get message
    print(data.decode()[0:3])

    connection.send("HTTP/1.1 200 OK\r\n".encode())
    connection.close
