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


def result(x, y, board):
    # need exceptions later


    # check if the coordinates match a boat
    # if it doesn't, print "Miss"
    # if it does, prints "Hit", replaces the boat letter with a hit 'X'
    # then checks if there are any more letters of that boat type
    # (if the boat sunk or not)
    # if none are found, print Sunk
    if board[x][y] != '_':
        print("Hit " + board[x][y] + "!")
        temp = board[x][y]
        board[x][y] = 'X'
        if(not any(temp in sublist for sublist in board)):
            print("Sunk!")



    else:
        print("Miss!")

    # just a pretty way to print the board
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in board]))


    # returns the updated board
    return board
