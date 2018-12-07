# CSCI 3800 Final Project
# Group: ScrapeyDo
# Group leader: Yuzhe Lu
# Group members: Yuzhe Lu, David Oligney, Prinn Prinyanut, Eric Slick, Patrick Tate

# Post class written by Yuzhe Lu, modifications by Patrick Tate
# Post class to hold ouput from Scraper class
class Post:

    # *** member variables ***
    __title = ""
    __likes = ""
    __author = ""
    # *** member variables ***

    # default initializer
    def __init__(self, title_, author_, likes_):
        self.__title = title_
        self.__likes = likes_
        self.__author = author_

    # getters
    def getTitle(self):
        return self.__title
    def getLikes(self):
        return self.__likes
    def getAuthor(self):
        return self.__author

    def __repr__(self):
        return "Title: " + str(self.getTitle()) + " Author: " + str(self.getAuthor()) + " Likes: " + str(self.getLikes())

# TwitterPost class written by Eric Slick
class twitterPost(Post):
    def __init__(self, actual_name_, screen_name_, tweet_, favorites_, retweets_):
        self.actual_name = actual_name_
        self.screen_name = screen_name_
        self.tweet = tweet_
        self.favorites = favorites_
        self.retweets = retweets_


    def getActualName(self):
        return self.actual_name

    def getScreenName(self):
        return self.screen_name

    def getFavorites(self):
        return self.favorites

    def getRetweets(self):
        return self.retweets

    def returnTweet(self):
        return "Printing tweets from: " + str(self.getActualName()) + ":    "+str(self.tweet) + "||    Favorites: "+str(self.getFavorites()) + "||   Retweets: "+str(self.getRetweets())

    def __repr__(self):
        return "Printing tweets from: " + str(self.getActualName()),"\n------------------------------","\nTweet: "+str(self.tweet),"\nFavorites: "+str(self.getFavorites()),"\nRetweets: "+str(self.getRetweets())