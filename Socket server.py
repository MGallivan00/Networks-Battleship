import socket
import sys
import copy
# TODO: print statements clean up # Julian
# TODO: Add comments # Julian
# TODO: argument that gets the opponent board # Julian

def init(): # checks if the number of arguments is correct

    if (len(sys.argv) == 1):
        print("Please enter a Port number and a text file.")
        exit()
    if(len(sys.argv) == 2):
        print("Please enter a second argument.")
        exit()
    if(len(sys.argv) > 3):
        print("Please enter only 2 arguments.")
        exit()


def printboard(board, game): # prints the board on the browser (uses HTML/CSS)
    if (game == False):
        cont = '<table style="border:1px solid black; width:50%;text-align:center">'
        for i in range(len(board)):
            cont += '<tr style="border:1px solid black;height:50%; text-align:center">'
            for j in range(len(board[i])):
                cont += '<td style="border:1px solid black;height:50%; text-align:center">'
                cont += board[i][j]
                cont += "</td>"
            cont +="</tr>"
        cont += "</table>"
    elif (game == True):
        cont = '<table style="border:1px solid black; width:50%;text-align:center">'
        for i in range(len(board)):
            cont += '<tr style="border:1px solid black;height:50%; text-align:center">'
            for j in range(len(board[i])):
                cont += '<td style="border:1px solid black;height:50%; text-align:center">'
                cont += '<a href=http://127.0.0.1:8080/game.html/'+str(i)+str(j)+'>Attack</a>'
                cont += "</td>"
            cont +="</tr>"
        cont += "</table>"
    return cont

def pboard(board):
    for x in board:
        print(x)

def boatcheck(boat):
    b = ""
    if(boat == 'D'):
        b = "Destroyer"
    elif(boat == 'B'):
        b = "Battleship"
    elif(boat == 'C'):
        b = "Carrier"
    elif(boat == 'R'):
        b = "Cruiser"
    else:
        b = "Submarine"

    return b

def result(x, y, board, records):

    result = ""
    records[x][y] = 'X'
    if board[x][y] != '_': # if Hit
        temp = board[x][y]
        print("The opponent fired and it hit a " + boatcheck(temp) + "!")
        result = "hit=1"
        board[x][y] = 'X'

        if(not any(temp in sublist for sublist in board)): # check if boat sunk
            print("The opponent sunk the " + boatcheck(temp) + "!")
            result += "\&sink=" + temp
    else:
        print("The opponent fired and it missed!")
        result = "hit=0"

    print("\nThis is the current state of your board:\n")
    pboard(board)
    print("\nHere is the record of your opponent's attacks:\n")
    pboard(records)

    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in records])) # error

    return result

def endgame(board):
    # need to find a way to end the game...
    if(not any('D' in sublist for sublist in board) and not any('C' in sublist for sublist in board) and
    not any('S' in sublist for sublist in board) and not any('R' in sublist for sublist in board) and
    not any('B' in sublist for sublist in board)):
        print("\n\nThe opponent knocked down all ships! The opponent wins!")
        print("Thank you for playing our game! To play again please restart the server.\n")
        return "win"
    else:
        return ""


def main():
    init()
    # assigning arguments into variable
    port_number=sys.argv[1]
    file_board=sys.argv[2]

    # import the board from file
    with open(file_board) as text:
        board = [list(line.strip()) for line in text]

    # create the record of hit (oppenent board) from the own board layout and empty it
    records = copy.deepcopy(board)
    for i in range(len(records)):
        for j in range(len(records[i])):
            records[i][j]="_"


    print("\n\tWelcome to Battleship! Let's start the game.\n")
    print("This is the current state of your board:\n")
    pboard(board)
    print("\nHere is the record of your opponent's attacks:\n")
    pboard(records)
    print("\nWaiting for opponent to fire...\n")


    # socket internet address family, with TCP. Binds with port number entered
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind (("127.0.0.1", (int(port_number))))
    s.listen(1)
    while True:
        win = ""
        connection, address = s.accept()
        request = connection.recv(99999).decode("utf-8") # receives encoded message and decodes it to request

        if(request[0] == 'P'):
            print("(Request type: POST (supported))")
            # print(request)
            xcor = int(request[-5:-4]) # get xcor and ycor from request message
            ycor = int(request[-1:])

            if xcor > len(board) or ycor > len(board) or xcor < 0 or ycor < 0:
                connection.sendall(str.encode("HTTP/1.1 404 Not Found\r\n\n"))

            elif board[xcor][ycor] == 'X':
                connection.sendall(str.encode("HTTP/1.1 410 Gone\r\n\n"))

            else:
                r = result(xcor, ycor, board, records)
                win = endgame(board)
                if(win == "win"):
                    answer = "HTTP/1.1 200 OK\r\n\n" + win
                else:
                    answer = "HTTP/1.1 200 OK\r\n\n" + r
                connection.sendall(str.encode(answer))

        elif(request[0] == 'G'): # for GET requests
            print("(Request type: GET (supported))")
            space = request.find(" ", 5) # finds the second space in the request message
            path = request[4:space] # gathers the path with the space index
            # show all coordinates that have been fired on (client perspective)
            if (path == "/opponent_board.html"):
                cont = printboard(records, False)
            # show current state of the board (server perspective)
            elif (path == "/own_board.html"):
                cont = printboard(board, False)
            elif (path == "/game.html"):
                cont = printboard(board, True)
            else:
                print(path[-1])
                print(path[-2])
                cont = "Path does not exit"

            answer = "HTTP/1.1 200 OK\r\n\n" + cont
            connection.sendall(str.encode(answer))

        else:
            connection.sendall(str.encode("HTTP/1.1 400 Bad Request\r\n\n"))

        connection.close()
        if(win == "win"):
            break;

    #### END While loop

    s.close()

main()
