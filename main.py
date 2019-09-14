import socket
import requests


def main():
    print("BattleShip game")
    print("Here is your board\n");

    # open text file, create board array, and
    # strip each character from the line to its own item in the array
    with open("own_board.txt") as text:
        board = [list(line.strip()) for line in text]

    while 1:
        x, y = fire() # fire returns an x value and a y value
        board = result(int(x), int(y), board) # returns a new board array


def fire(): # client function

    # ask for coordinates
    # split the coordinates
    # add the specific url content
    coordinates = input("Choose your next coordinates to bomb: ")
    coordinates = coordinates.split(" ")
    content = "x=" + coordinates[0] + "&y=" + coordinates[1]
    print(content)

    # need to send coordinates to server

    return coordinates[0], coordinates[1]


def result(x, y, board): # server function
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




main()
