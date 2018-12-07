# CSCI 3800 Final Project
# Group: ScrapeyDo
# Group leader: Yuzhe Lu
# Group members: Yuzhe Lu, David Oligney, Prinn Prinyanut, Eric Slick, Patrick Tate

# User class written by Prinn Prinyanut and Patrick Tate, tested by David Oligney
# class to model a User object on
# user has a name, password, keyword to scrape for, and a list of posts(scrape results)
class User:
    # *** member variables ***
    # login credentials
    __name = ""
    __password = ""
    # keywords user has searches for during current session
    __searchHistory = []
    # keyword the use wants to scrape for
    __keyword = ""
    # list to hold the results of the scape
    __posts = []

    # *** member variables ***

    # default initializer, optional: parameters name string and password string
    # empty lists for searchHistory and posts instantiated
    def __init__(self, name="", password=""):
        self.__name = name
        self.__password = password
        self.__searchHistory = []
        self.__keyword = ""
        self.__posts = []

    # getters/setters
    def setName(self, name):
        self.__name = name

    def setPassword(self, password):
        self.__password = password

    def setKeyword(self, keyword):
        self.__keyword = keyword

    def getName(self):
        return self.__name

    def getPassword(self):
        return self.__password

    def getKeyword(self):
        return self.__keyword

    def getPosts(self):
        return self.__posts

    def getSearchHistory(self):
        return self.__searchHistory

    # add line of text to posts list
    def addPost(self, line):
        self.__posts.append(line)

    # add keyword to user's searchHistory list
    def addHistory(self, keyword):
        self.__searchHistory.append(keyword)


