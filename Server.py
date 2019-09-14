import socket
import os

HOST = '127.0.0.1'
PORT = 8080

print("Battleship Game\n")
F = open('text_board.txt', "r");
text = F.readlines()
print("Here is your board");
for x in text:
    print(x)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(b'Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
