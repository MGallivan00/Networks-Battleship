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


def winpage(): # formats the win page to be slightly more exciting
    html = """<!DOCTYPE html><html><head><title>Battleship</title></head><body>
    <div style="display:inline-flex;justify-content:center;align-items:center;width:100vw;height:100vh;
    text-align: center;"><h2>You Won!<br>You knocked down all ships!<br>
    Thank you for playing our game!<br>To play again please restart the server.
    </h2></div></body></html>"""
    css = """<style type="text/css">
body {
  font-family: georgia, serif;
  font-size: x-large;
  color:#ff9900;
  background-image: url("https://nationalinterest.org/sites/default/files/styles/desktop__1260_/public/main_images/uss_new_jersey_6219214852_0.jpg?itok=iGTZnCsr");
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  }
</style>"""
    html += css
    return html


def printboard(board, game): # prints the board on the browser (uses HTML/CSS)
    style = 'style="border:1px solid black; width:50%; text-align:center";>' # styling of the board
    link = '<a style="text-decoration:none;color:black;"href=http://127.0.0.1:8080/game.html/'
    hitlink = '<a style="text-decoration:none;color:red;"href=http://127.0.0.1:8080/game.html/'
    css = """<style type="text/css">
    body {
      font-family: georgia, serif;
      font-size: x-large;
      color:#ff9900;
      background-image: url("https://nationalinterest.org/sites/default/files/styles/desktop__1260_/public/main_images/uss_new_jersey_6219214852_0.jpg?itok=iGTZnCsr");
      background-position: center;
      background-repeat: no-repeat;
      background-size: cover;
    }
    .center {
        display: flex-inline;
        justify-content: center;
        align-items: center;
        width: 100vw;
        height: 100vh;
    }

    </style>"""

    cont = "<!DOCTYPE html><html><head><title>Battleship</title></head><body>"
    cont += css
    if (game == False):
        cont += '<div class="center"><table ' + style
        for i in range(len(board)):
            cont += '<tr ' + style
            for j in range(len(board[i])):
                cont += '<td ' + style
                cont += board[i][j]
                cont += "</td>"
            cont +="</tr>"
        cont += "</table></div>"

    else: # changes the board as the user attack
        cont += '<div class="center"><table ' + style
        for i in range(len(board)):
            cont += '<tr ' + style
            for j in range(len(board[i])):
                cont += '<td ' + style
                if (board[i][j] != 'X'):
                    cont += link + str(i) + str(j) + '>Attack</a>'
                else:
                    cont += hitlink + str(i) + str(j) + '>Shot</a>'
                cont += "</td>"
            cont +="</tr>"
        cont += "</table></div>"
    cont += "</body></html>"
    return cont

def pboard(board):
    for x in board:
        print(x)

def boatcheck(b): # defines each ship's name from the character
    boat = ""
    if(b == 'D'):
        boat = "Destroyer"
    elif(b == 'B'):
        boat = "Battleship"
    elif(b == 'C'):
        boat = "Carrier"
    elif(b == 'R'):
        boat = "Cruiser"
    else:
        boat = "Submarine"

    return boat

def result(x, y, board, records): # responds with a number of outcomes to the client

    result = ""
    records[x][y] = 'X'
    if board[x][y] != '_': # if Hit
        temp = board[x][y]
        print("The opponent fired and it hit a " + boatcheck(temp) + "!")
        result = "hit=1" + temp
        board[x][y] = 'X'

        if(not any(temp in sublist for sublist in board)): # check if boat sunk
            print("The opponent sunk the " + boatcheck(temp) + "!")
            result += "\&sink=" + temp
    else:
        print("The opponent fired and it missed!")
        result = "hit=0" + 'M'

    print("\nThis is the current state of your board:\n")
    pboard(board)
    print("\nHere is the record of your opponent's attacks:\n")
    pboard(records)

    return result

def checkEndGame(board): # checks if the game is over
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
            equals = request.find('=') # index foe first '='
            amp = request.find('&')
            xcor = request[equals+1:amp]
            ycor = request[amp+3:]

            if not xcor.isdigit() or not ycor.isdigit(): # if x or y is not a number
                connection.sendall(str.encode("HTTP/1.1 400 Bad Request\r\n\n"))
                continue

            xcor = int(xcor)
            ycor = int(ycor)

            if xcor > len(board) or ycor > len(board) or xcor < 0 or ycor < 0: # if out of bounds
                connection.sendall(str.encode("HTTP/1.1 404 Not Found\r\n\n"))

            elif board[xcor][ycor] == 'X': # already hit
                connection.sendall(str.encode("HTTP/1.1 410 Gone\r\n\n"))

            else: # if successful (no errors)
                r = result(xcor, ycor, board, records)
                win = checkEndGame(board)
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
            if (path == "/opponent_board.html" or path == "/opponent_board.html/"):
                cont = printboard(records, False)

            # show current state of the board (server perspective)
            elif (path == "/own_board.html" or path == "/own_board.html/"):
                cont = printboard(board, False)

            elif (path == "/game.html" or path == "/game.html/"):
                print("web client start")
                cont = printboard(board, True)

            elif (path[0:10] == "/game.html" and isinstance(int(path[-1]), int) and isinstance(int(path[-2]), int)):
                print("web client attack")
                print(path[-1])
                print(path[-2])
                hit = result(int(path[-2]),int(path[-1]), board, records)
                win = checkEndGame(board)

                if(win == "win"):
                    cont = winpage()

                else:
                    cont = printboard(records, True)
                    if (hit[:-1] == "hit=1"):
                        cont += "You hit!"
                    else:
                        cont += "You missed!"

            else:
                cont = "non existent path"
            answer = "HTTP/1.1 200 OK\r\n\n" + cont
            connection.sendall(str.encode(answer))



        connection.close()
        if(win == "win"):
            break;

    #### END While loop

    s.close()

main()
