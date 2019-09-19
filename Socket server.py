import socket
import sys
import copy #add to import to actualy copy board and not to cross reference it when creating records (opponent board)
# TODO: Error in opponent_board [ALMOST DONE!]
# TODO: print statements clean up [ALMOST DONE!]
# TODO: error handling for arguments in terminal [DONE!]
# TODO: Add comments [DONE!]
# TODO: test if reponse is correctly formatted (wireshark)
# TODO: argument that gets the opponent board #opponent board fixed


def result(x, y, board, records):

    result = ""
    records[x][y] = 'X'
    if board[x][y] != '_': # if Hit
        print("Hit " + board[x][y] + "!")
        result = "hit=1"
        temp = board[x][y]
        board[x][y] = 'X'

        if(not any(temp in sublist for sublist in board)): # check if boat sunk
            print("Sunk!")
            result += "\&sink=" + temp
    else:
        print("Miss!")
        result = "hit=0"




    print("Here is your board:\n")
    for x in board:
        print(x)
    print("\n")
    print("Here is the record of the oponent attacks :\n")
    for x in records:
        print(x)
    print("\n")

    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in records])) # error

    return result
##############

def main():


    # checks if the number of arguments is correct
    if (len(sys.argv) == 1):
        print("Please enter a Port number and a text file.")
        exit()
    if(len(sys.argv) == 2):
        print("Please enter second argument.")
        exit()
    if(len(sys.argv) > 3):
        print("Please enter the right amount of arguments.")
        exit()

    # assigning arguments into variable
    print(sys.argv)
    port_number=sys.argv[1]
    file_board=sys.argv[2]

    # import the board from file
    with open(file_board) as text:
        board = [list(line.strip()) for line in text]
    #create the record of hit (openent board) from the own board layout and empty it
    records = copy.deepcopy(board)
    for i in range(len(records)):
            for j in range(len(records[i])):
                       records[i][j]="_"


    print("BattleShip game")
    print("Here is your board:\n")
    for x in board:
        print(x)
    print("\n")
    print("Here is the record of the oponent attacks :\n")
    for x in records:
        print(x)

    ##format to send the fire result
    # post_format         POST / HTTP/1.1
    #                     Host: 127.0.0.1
    #                     Content-Type: application/x-www-form-urlencoded
    #                     Content-Length: 27
    #
    #                     field1=value1&field2=value2

    # socket internet address family, with TCP. Binds with port number entered
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind (("127.0.0.1", (int(port_number))))
    s.listen(1)
    while True:
        connection, address = s.accept()
        request = connection.recv(99999).decode("utf-8") # receives encoded message and decodes it to request
        print("request:", request)
        if(request[0] == 'P'):
            print("Request type: POST (supported)")
            print(request)
            xcor = int(request[-5:-4]) # get xcor and ycor from request message
            ycor = int(request[-1:])

            # will need to revisit these responses:
            # what does he mean by not formatted correctly?
            if xcor < 0 or ycor < 0:
                connection.sendall(str.encode("HTTP/1.1 400 Bad Request\r\n\n"))

            elif xcor > len(board) or ycor > len(board):
                connection.sendall(str.encode("HTTP/1.1 404 Not Found\r\n\n"))

            elif board[xcor][ycor] == 'X':
                connection.sendall(str.encode("HTTP/1.1 410 Gone\r\n\n"))

            else:
                r = result(xcor, ycor, board, records)
                answer = "HTTP/1.1 200 OK\r\n\n" + r
                connection.sendall(str.encode(answer))

        elif(request[0] == 'G'): # for GET requests
            space = request.find(" ", 5) # finds the second space in the request message
            path = request[4:space] # gathers the path with the space index

            # show all coordinates that have been fired on (client perspective)
            if (path == "/opponent_board.html"):
                cont = "\n".join(['\t'.join([str(cell) for cell in row]) for row in records])

            # not quite sure if this is correct yet. Requires comformation.
            # show current state of the board (server perspective)
            elif (path == "/own_board.html"):
                cont = "\n".join(['\t'.join([str(cell) for cell in row]) for row in board])
            else:
                cont = "Path does not exit"

            print("Request type: GET (supported)")
            answer = "HTTP/1.1 200 OK\r\n\n" + cont
            connection.sendall(str.encode(answer))


        connection.close()
    #### END While loop

    s.close()

main()
