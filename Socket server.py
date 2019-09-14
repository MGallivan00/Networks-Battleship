import socket
import sys

#check for argument
if not (sys.argv) :
    print("Usage 1 argument")
    exit()

#putting argument into variable
port_number=sys.argv[1]
file_board=sys.argv[2]



#result function
def result(x, y, board):
    # need exceptions later
    result = "null"

    # check if the coordinates match a boat
    # if it doesn't, print "Miss"
    # if it does, prints "Hit", replaces the boat letter with a hit 'X'
    # then checks if there are any more letters of that boat type
    # (if the boat sunk or not)
    # if none are found, print Sunk
    if board[x][y] != '_':
        result ="Hit " + board[x][y] + "!"
        temp = board[x][y]
        board[x][y] = 'X'
        if(not any(temp in sublist for sublist in board)):
            result ="Sunk!"
    else:
        result = "Miss!"

    # just a pretty way to print the board
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in board]))


    # returns the updated board
    return result
##########

print("BattleShip game\n")

with open(file_board) as text:
    board = [list(line.strip()) for line in text]
print("Here is your board");
for x in board:
    print(x)

##format to send the fire result
post_format = """POST /test HTTP/1.1
Host: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 27

field1=value1&field2=value2"""
letter_o=post_format[28]
print(letter_o);
#


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind (("127.0.0.1", (int(port_number))))
s.listen(1)
while 1:
    connection, address = s.accept()
    data = connection.recv(99999)
    #print(data)
    print(data.decode()[0])
    if(data.decode()[0] == 'P'):
        print("Is a post request, supported")
        print(data.decode())
        result=result(1, 1, board);
        print(result);
        #if(result ==):

    elif(data.decode()[0] == 'G'):
        print("Is a get request, Not supported")
    connection.close
