
import socket
import sys



def init(): # checks if number of arguments are valid

    if (len(sys.argv) == 1):
        print("Please respect synthax python3 client.py address portnumber xcoordinate ycoordinate.")
        exit()
    if(len(sys.argv) > 1 and len(sys.argv) < 5):
        print("Please enter 4 arguments.")
        exit()
    if(len(sys.argv) > 5):
        print("Please enter only 4 arguments.")
        exit()
    if(not isinstance(int(sys.argv[3]), int) and (not isinstance(int(sys.argv[4]), int))):
        print("d")
        exit()

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


def fire():

    # format:
    # $python3 client.py 127.0.0.1 8080  5    7
    #          [0]          [1]   [2]  [3]  [4]

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    xcor = sys.argv[3]
    ycor = sys.argv[4]

    contentlength = 5+len(str(xcor))+len(str(ycor))
    content = "POST \nHost: " + HOST + "\nContent-Type: misc\nContent-Length: " + str(contentlength) + "\n\n" + "x=" + xcor + "&y=" + ycor

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(content))
        msg = s.recv(1024)
        message = msg.decode("utf-8")

        if(message[-3:] == "win"):
            print("\n\nYou destroyed all ships! You Won!")
            print("Thank you for playing our game!")
            print("The server has shut down.\n")
            exit()

        print()
        code = message[9:12]
        if(code == "200"): # OK
            if(message[-6:-2] == "sink"):
                print("You hit and sunk a " + boatcheck(message[-1:]) + "!")
            elif(message[-2:-1] == "1"):
                print("You hit a " + boatcheck(message[-1:]) + "!")
            else:
                print("You missed your shot!")

        elif(code == "404"): # NOT FOUND
            print("You need to ender coordinates on the board!")

        elif(code == "410"): # DONE
            print("You already hit this location!")

        else: # BAD REQUEST
            print("Something went wrong... \n(Error 400)\n")

        print()

init()
fire() # send fire coordinates to server
