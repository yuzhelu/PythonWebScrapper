# CSCI 3800 Final Project
# Group: ScrapeyDo
# Group leader: Yuzhe Lu
# Group members: Yuzhe Lu, David Oligney, Prinn Prinyanut, Eric Slick, Patrick Tate

# first run server.py, then run client.py to connect as many different clients to the Server as you want

from socket import socket, AF_INET, SOCK_STREAM # because we need sockets to connect to clients
import threading # multi-thread the clients
#import sys not sure if we will need this or not, works with it uncommented so...
from User import User # because Server has a list of users
from Scraper import RedditScraper, twitterScraper
import pickle  # to read in pickled/serialized posts

# Server class written by Prinn Prinyanut and Patrick Tate, tested by David Oligney
# Server class to handle multiple clients
# file is run by instantiating a Server object and calling member function run() at the bottom of this file
# Server object stays open and listens for clients
# Server object can handle multiple clients and takes advantage of multi-threading
# ********************************************************************************
# run() method calls the handler method which takes the connection and address as paramters
# from there, a client is greeted with an inital menu screen to create an account or login
class Server:

    # *** member variables ***
    # socket to bind and listen for clients
    __serversocket = socket(AF_INET, SOCK_STREAM)
    # list of client connections, when client chooses to disconnect, connection is removed from list and connection is closed
    __connections = []
    # list of User objects, will be a dictionary {} that is serialized and read in
    __clients = []
    # *** member variables ***

    # default initializer, listen for clients on socket 5000
    def __init__(self):
        self.__serversocket.bind(('localhost', 5000))
        self.__serversocket.listen(5)
        self.__connections = []
        self.__clients = []

    # getters/setters
    def getClients(self):
        return self.__clients

    # add user object to list of connections/users
    def addClient(self, user):
        self.__clients.append(user)

    # only function we need to call to start the server while it waits for clients
    # will run this in a main/App file later, but for now just runs at the bottom of this file
    def run(self):
        # wait for clients, need to figure out the best way to end this loop other than pressing the "stop" button
        while True:
            # accept connection from client
            connection, address = self.__serversocket.accept()
            # add connection to the list of connections self.connections
            self.__connections.append(connection)
            # thread for this connection, call self.handler() function
            cthread = threading.Thread(target=self.handler, args=(connection, address))
            cthread.daemon = True
            cthread.start()
            # print the address for reference
            print(str(address[0]) + ':' + str(address[1]) + " connected")

    # calls initialMenu(connection, address) function to display the first menu to the user
    def handler(self, connection, address):
        self.initialMenu(connection, address)

    # first menu client/user sees when connecting to server
    # takes connection and address variables from serversocket.accept() function in run(self)
    def initialMenu(self, connection, address):
        self.loadUsers()
        while True:
            # initial menu message for user/client
            initialMsg = "Welcome to the Scraping Server\n" \
                         "Choose an option\n" \
                         "1: create account\n" \
                         "2: sign in\n" \
                         "3: disconnect"
            # send itial menu message to user
            connection.send(bytes(initialMsg, 'utf-8'))
            # receive input from the user on which option
            data = connection.recv(1024)

            # convert client input to string
            clientOption1 = str(data, 'utf-8')

            # switch on user input option
            # 1 = create account
            # calls createAccount() function
            # account user name must not already exist in self.clients list
            if clientOption1 == "1":
                # print message on server for reference
                print("client chose create account")
                # call createAccount function with connection, address info
                self.createAccount(connection, address)
                # can delete lines below, printing on the server the user names in self.clients just for reference
                for user in self.__clients:
                    print(user.getName())

            # client wants to sign in
            # password needs to be validated in list/dictionary of users
            # *** need to write this function ***
            elif clientOption1 == "2":
                print("client chose sign in")
                self.signIn(connection, address)

            # client wants to disconnect
            # remove client from list of connections and close connection
            # *** need to add this as a case, and have last else as default catch bad input ***
            elif clientOption1 == "3":
                self.__connections.remove(connection)
                print(str(address[0]) + ':' + str(address[1]) + " disconnected")
                connection.close()
                break

            # default catch
            else:
                invalidInput = "*** invalid input, try again\n"
                print(invalidInput)
                connection.send(bytes(invalidInput, 'utf-8'))


            # this is a catch if there is no more connections of data incoming
            if not data:
                self.connections.remove(connection)
                print(str(address[0]) + ':' + str(address[1]) + " disconnected")
                connection.close()
                break

    # used in conjunction with createAccount function
    # as soon as a new user is created, send their name and password to the userData.txt file
    # prints name and password to file in format of name followed by space followed by password:
    # example: userName1 password123
    def updateUserList(self, user):
        info = user.getName() + " " + user.getPassword() + "\n"
        print(info)
        userData = open("userData.txt", 'a+')
        userData.write(info)
        userData.close()


    # load list of users as soon as server starts
    # loads name and password to file in format of name followed by space followed by password:
    # example: userName1 password123
    def loadUsers(self):
        userData = open("userData.txt", "r")
        userData1 = userData.readlines()
        for line in userData1:
            user = User()
            info = line
            dataList = info.split(" ")
            name = dataList[0]
            password = dataList[1]
            user.setName(name)
            password = password.rstrip()
            user.setPassword(password)
            self.addClient(user)
        print(self.__clients)
        userData.close()

    # client must successfully sign in before they can scrape any data
    # first they must enter a valid user name
    # then the client enters the password which must match that user's password
    # if password is correct, main menu function is called for scraping options
    def signIn(self,connection, address):
        # msg to send client
        name = "Enter your username\n"
        # send msg to client
        connection.send(bytes(name, 'utf-8'))
        # receive name
        name = connection.recv(1024)
        # convert name to a string, always utf-8 encoding
        sname = str(name, 'utf-8')
        print(sname)  # print for reference
        # check if user name exists
        validLogin = False
        for user in self.__clients:
            if user.getName() == sname:
                successMsg = "valid username"
                connection.send(bytes(successMsg, 'utf-8'))
                choosePassword = "Enter your password: \n"
                connection.send(bytes(choosePassword, 'utf-8'))
                password = connection.recv(1024)
                spassword = str(password, 'utf-8')
                # check if password matches
                if user.getPassword() == spassword:
                    # call main menu function
                    print("main menu display")
                    # pass user to function
                    validLogin = True
                    validUser = user
                    #self.mainMenu(connection,address,user)
                    break
                else:
                    wrongPw = "*** invalid password, try again ***"
                    connection.send(bytes(wrongPw, 'utf-8'))
                print(spassword)
            else:
                # check next user in self.clients
                pass
        # if validLogin == True, run scraping menu
        if validLogin:
            self.mainMenu(connection, address, validUser)

        # print message to client if no user with that name
        if not self.checkUsername(sname):
            invalidName = "*** no user with that name, try again ***"
            connection.send(bytes(invalidName, 'utf-8'))

    # check if user name exists, return True is username exists
    def checkUsername(self, name):
        for user in self.__clients:
            if user.getName() == name:
                return True
        return False

    # main menu display after user signs in
    def mainMenu(self, connection, address, user):
        # run menu
        while True:
            # initial menu message for user/client
            initialMsg = "Welcome " + user.getName() + "\n" \
                         "Choose an option\n" \
                         "1: enter keyword to scrape reddit\n" \
                         "2: enter a twitter handle to scrape twitter\n" \
                         "3: print all scrape results\n" \
                         "4: search posts by title\n" \
                         "5: save all results to file\n" \
                         "6: return to previous menu"
            # send itial menu message to user
            connection.send(bytes(initialMsg, 'utf-8'))
            # receive input from the user on which option
            data = connection.recv(1024)

            # convert client input to string
            clientOption1 = str(data, 'utf-8')

            if clientOption1 == "1":
                print("scrape reddit")
                self.askKeyword(connection,address,user)

            elif clientOption1 == "2":
                self.scrapeTwitter(connection,address,user)
                print("scrape twitter")

            elif clientOption1 == "3":
                print("print all")
                self.printResults(connection,address,user)

            elif clientOption1 == "4":
                print("search posts by title")
                self.searchResults(connection,address,user)

            elif clientOption1 == "5":
                print("save results")
                self.saveToFile(connection,address,user)

            elif clientOption1 == "6":
                break
            # catch bad input
            else:
                print("*** invalid option ***")

    # save the user/client's posts to a txt file
    # user/client may scrape on many keywords in one session, and all posts are saved to user.posts
    def saveToFile(self, connection, address, user):
        filePrompt = "enter the name of the file you want to save results as"
        # send itial menu message to user
        connection.send(bytes(filePrompt, 'utf-8'))
        # receive input from the user on which option
        data = connection.recv(1024)
        # convert client input to string
        fileName = str(data, 'utf-8')
        fileName = fileName + ".txt"
        userFile = open(fileName, 'a+')
        for line in user.getPosts():
            userFile.write(line+"\n")
        userFile.close()

    # user enters a word to search their scraped results for
    def searchResults(self,connection, address, user):
        searchPrompt = "enter word to search for in reddit results"
        # send itial menu message to user
        connection.send(bytes(searchPrompt, 'utf-8'))
        # receive input from the user on which option
        data = connection.recv(1024)
        # convert client input to string
        searchWord = str(data, 'utf-8')
        for post in user.getPosts():
            if searchWord in post:
                print(post)
                connection.send(bytes(post+"\n", 'utf-8'))

    # print user's posts in user.posts
    def printResults(self, connection, address, user):
        for post in user.getPosts():
            connection.send(bytes(post+"\n", 'utf-8'))

    # scrape twitter and add post to users list
    # print twitter results to client
    def scrapeTwitter(self,connection,address,user):
        twitterHandle = "Enter the twitter user's handle you want to scrape"
        # send itial menu message to user
        connection.send(bytes(twitterHandle, 'utf-8'))
        # receive input from the user on which option
        data = connection.recv(1024)
        # convert client input to string
        keyword = str(data, 'utf-8')
        if keyword is not None:
            pass
        else:
            failure = "Twitter handle does not exist!"
            connection.send(bytes(failure+"\n", 'utf-8'))
        user.addHistory(keyword)
        user.setKeyword(keyword)

        success = "Twitter handle: " + keyword + " successfully added to your search history, press 3 to print results"
        connection.send(bytes(success+"\n", 'utf-8'))
        print(keyword)
        twit = twitterScraper(keyword)
        unpickled_tweets = pickle.loads(twit.runScrapper())

        twit = ""
        for post in unpickled_tweets:
            twit = str(post.returnTweet())
            user.addPost(twit)
            print(twit)


    # get the keyword the user wants to search for and run a scrape on that keyword
    # save scrape results to user.posts and print to client
    def askKeyword(self, connection, address, user):
        keyPrompt = "enter the keyword you want to scrape for"
        # send itial menu message to user
        connection.send(bytes(keyPrompt, 'utf-8'))
        # receive input from the user on which option
        data = connection.recv(1024)
        # convert client input to string
        keyword = str(data, 'utf-8')
        user.addHistory(keyword)
        user.setKeyword(keyword)
        success = "keyword: " + keyword + " successfully added to your search history, press 3 to print results"
        connection.send(bytes(success, 'utf-8'))
        print(keyword)
        sc = RedditScraper(keyword)
        # sc.runScrapper()

        unpickled_subs = pickle.loads(sc.runScrapper())
        scrapeResults = ""
        for line in unpickled_subs:
            scrapeResults = scrapeResults + str(line) + "\n"
            print(line)

        post = scrapeResults.split("\n")
        for word in post:
            print(word)
            user.addPost(word)


    # void function to create a user account
    # creates a User object based on client input and adds user to self.clients list/dictionary
    # user is prompted to enter another name if user name alerady exists in self.clients
    def createAccount(self, connection, address):
        # msg to send client
        chooseName = "Enter a username (must not be taken)\n"
        # send msg to client
        connection.send(bytes(chooseName, 'utf-8'))
        # receive name
        name = connection.recv(1024)
        # convert name to a string, always utf-8 encoding
        sname = str(name, 'utf-8')
        print(sname) # print for reference

        # check if name exists in self.clients
        valid = self.isValid(sname)
        # if name is valid, prompt for a password, create a User object and add to self.clients
        if valid:
            successMsg = "valid username"
            connection.send(bytes(successMsg, 'utf-8'))
            choosePassword = "Enter a password: \n"
            connection.send(bytes(choosePassword, 'utf-8'))
            password = connection.recv(1024)
            spassword = str(password, 'utf-8')
            accCreated = "account successfully created, now sign in\n"
            connection.send(bytes(accCreated, 'utf-8'))
            print(spassword)
            user = User(sname, spassword)
            self.addClient(user)
            self.updateUserList(user)
        # else prompt user to enter another name
        else:
            errMsg = "Name taken, try again"
            connection.send(bytes(errMsg, 'utf-8'))

    # returns True if name isn't in self.clients
    # returns False if name is equal to user.name in self.clients
    def isValid(self, name):
        validName = True
        # if self.clients list is empty, no user names exist yet, return True
        if len(self.__clients) == 0:
            print("zero size")
            return True

        # check list of users to see if user name already exists
        # return False if user name already exists
        for user in self.__clients:
            if user.getName() == name:
                return False

        # return True is all above checks passed
        return validName

# instantiate Server object
server = Server()
# run the whole party
server.run()
