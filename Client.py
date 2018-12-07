# CSCI 3800 Final Project
# Group: ScrapeyDo
# Group leader: Yuzhe Lu
# Group members: Yuzhe Lu, David Oligney, Prinn Prinyanut, Eric Slick, Patrick Tate

# Client class and file to be used in conjunction with server.py
# first run server.py, then run client.py to connect as many different clients to the Server as you want

import socket # so we can connect to the server
import threading # so we can take advantage of multi-threading

# Client class written by Prinn Prinyanut and Patrick Tate, tested by David Oligney
# Client class that connects to localhost server on port 5000
class Client:

    # *** member variables ***
    # create a socket object
    __client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __iThread = ""
    # *** member variables ***

    # initialize the client object and connect to localhost on port 5000
    # calls the self.sendKeyword() function to communicate to the Server
    def __init__(self):
        # connection to localhost on the port 5000
        self.__client_socket.connect(('localhost', 5000))
        # start a thread for the connection
        __iThread = threading.Thread(target=self.sendKeyword)
        __iThread.daemon = True
        __iThread.start()

        # receive input from Server
        # print input in client terminal
        while True:
            data = self.__client_socket.recv(1024)
            print(str(data, 'utf-8'))
            if not data:
                self.__client_socket.close()
                break

    # used to get a prompt on the client side and send msg to the Server
    def sendKeyword(self):
        while True:
            self.__client_socket.send(bytes(input(""), 'utf-8'))

# instantiate a client
client = Client()
