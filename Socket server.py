import socket
import sys

# TODO: Error in opponent_board
# TODO: print statements clean up
# TODO: error handling for arguments in terminal
# TODO: Add comments
#       http://localhost:5000/opponent_board.html



def result(x, y, board, records):

    result = "null"
    if board[x][y] != '_':
        print("Hit " + board[x][y] + "!")
        result = "hit=1"
        temp = board[x][y]
        board[x][y] = 'X'
        records[x][y] = 'X'
        if(not any(temp in sublist for sublist in board)):
            print("Sunk!")
            result += "\&sink=" + temp
    else:
        print("Miss!")
        result = "hit=0"

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in board]))
    print()
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in records])) # error

    return result
##############

def main():

    #check for argument
    if not (sys.argv[1]):
        print("Usage 1 argument")
        exit()

    #putting argument into variable
    print(sys.argv)
    port_number=sys.argv[1]
    file_board=sys.argv[2]


    with open(file_board) as text:
        board = [list(line.strip()) for line in text]
        records = board # error
        # join(['\t'.join([str(cell) for cell in row]) for row in records])
    for row in records:
        for cell in row:
            cell = " "

    print("BattleShip game")
    print("Here is your board:\n")
    for x in board:
        print(x)

    ##format to send the fire result
    post_format = """   POST / HTTP/1.1
                        Host: 127.0.0.1
                        Content-Type: application/x-www-form-urlencoded
                        Content-Length: 27

                        field1=value1&field2=value2 """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind (("127.0.0.1", (int(port_number))))
    s.listen(1)
    while True:
        connection, address = s.accept()
        request = connection.recv(99999).decode("utf-8") # receives encoded message and decodes it to request
        print("request:", request)
        if(request[0] == 'P'): # "for POST:" request[0] == 'P'
            print("Request type: POST (supported)")
            print(request)
            xcor = int(request[-5:-4])
            ycor = int(request[-1:])

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

        elif(request[0] == 'G'): # for GET
            space = request.find(" ", 5)
            path = request[4:space]
            if (path == "/opponent_board.html"):
                cont = "\n".join(['\t'.join([str(cell) for cell in row]) for row in records])

            elif (path == "/own_board.html"):
                cont = "\n".join(['\t'.join([str(cell) for cell in row]) for row in board])
            else:
                cont = "Path does not exit"

            print("Request type: GET (supported)")
            # content = "HTTP/1.1 200 OK\r\n\n" +
            answer = "HTTP/1.1 200 OK\r\n\n" + cont
            connection.sendall(str.encode(answer))


        connection.close()
    #### END While loop

    s.close()

main()
