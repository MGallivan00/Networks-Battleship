import socket
import sys

# TODO: we need to format the sends and responses as HTTP POST and HTTP response
# TODO: we need to error check the bounds/message and send a HTTP not found/HTTP bad requests
# TODO: We need to be able to update the current board and opponent board after each response
#       The client should be able to visually inspect each board at these addresses:
#       http://localhost:5000/own_board.html
#       http://localhost:5000/opponent_board.html



def result(x, y, board):

    result = "null"
    if board[x][y] != '_':
        print("Hit " + board[x][y] + "!")
        result = "hit=1"
        temp = board[x][y]
        board[x][y] = 'X'
        if(not any(temp in sublist for sublist in board)):
            print("Sunk!")
            result += "\&sink=" + temp
    else:
        print("Miss!")
        result = "hit=0"

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in board]))

    return result
##############

def main():

    #check for argument
    if not (sys.argv):
        print("Usage 1 argument")
        exit()

    #putting argument into variable
    print(sys.argv)
    port_number=sys.argv[1]
    file_board=sys.argv[2]


    with open(file_board) as text:
        board = [list(line.strip()) for line in text]
    print("BattleShip game")
    print("Here is your board:\n")
    for x in board:
        print(x)

    ##format to send the fire result
    post_format = """   POST /test HTTP/1.1
                        Host: 127.0.0.1
                        Content-Type: application/x-www-form-urlencoded
                        Content-Length: 27

                        field1=value1&field2=value2 """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind (("127.0.0.1", (int(port_number))))
    s.listen(1)
    while True:
        connection, address = s.accept()
        data = connection.recv(99999).decode("utf-8") # receives encoded message and decodes it to data
        print("Data:", data)
        if(True): # "for POST:" data[0] == 'P'
            print("Request type: POST (supported)")
            print(data)
            xcor = int(data[-5:-4])
            ycor = int(data[-1:])

            if xcor < 0 or ycor < 0:
                connection.sendall(str.encode("HTTP Bad Request"))

            elif xcor > len(board) or ycor > len(board):
                connection.sendall(str.encode("HTTP Not Found"))

            elif board[xcor][ycor] == 'X':
                connection.sendall(str.encode("HTTP Gone"))

            else:
                r = result(xcor, ycor, board)
                content = data + r
                print(content)
                connection.sendall(str.encode(content))

        elif(data[0] == 'G'): # for GET
            print("Request type: GET (unsupported)")


        connection.close()
        ans = input("Do you want to close the server? (yes/no)")
        if(ans == "yes"):
            break

    #### END While loop

    s.close()

main()
