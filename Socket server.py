import socket
import sys


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
    post_format = """POST /test HTTP/1.1
    Host: 127.0.0.1
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 27
    field1=value1&field2=value2"""
    letter_o=post_format[28]
    print(letter_o) # prints ':' ?



    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind (("127.0.0.1", (int(port_number))))
    s.listen(1)
    while 1:
        connection, address = s.accept()
        data = connection.recv(99999).decode("utf-8") # receives encoded message and decodes it to data
        print("Data:", data)
        # if(data[0] == 'P'):
        print("Request type: POST (supported)")
        print(data)
        xcor = int(data[-5:-4])
        ycor = int(data[-1:])
        r = result(xcor, ycor, board)
        content = data + r
        print(content)


        #if(result ==):

        #elif(data[0] == 'G'):
        print("Is a get request, Not supported")

        # we need to send the data now
        connection.sendall(str.encode(content))

        connection.close()
        ans = input("Do you want to close the server? (yes/no)")
        if(ans == "yes"):
            break

    s.close()

main()

# seeing if this works
