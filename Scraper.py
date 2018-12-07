# CSCI 3800 Final Project
# Group: ScrapeyDo
# Group leader: Yuzhe Lu
# Group members: Yuzhe Lu, David Oligney, Prinn Prinyanut, Eric Slick, Patrick Tate
# Reddit Scraper written by Yuzhe Lu, Twitter Scraper written by Eric Slick

#! usr/bin/env python3
from __future__ import print_function
import datetime as dt
import pandas as pd
import praw # to access reddit api
import pickle # to pickle/serialize submissions
import tweepy # for the twitter api

from Post import Post, twitterPost # Post object to hold the Reddit or Twitter post info

# parent class for Reddit and Twitter scrapers, written by Yuzhe Lu
class Scraper:

    # *** member variables
    __searchTerm = "" # term to scrape for
    __submissions = [] # list of submissions
    # *** member variables

    # term = "gaming" or any other keyword the user wants search for
    # initialize empty list submissions
    def __init__(self, term_):

        # private member variables
        self.__searchTerm = term_ # save search term. For reddit, this is the subreddit. For twitter, this is the user(?)
        self.__submissions = list() # list of submissions

    # getters/setters
    def getSearchTerm(self):
        return self.__searchTerm
    def getSubmissions(self):
        return self.__submissions

    # add Post object to submissions list
    def addPost(self, post):
        self.__submissions.append(post)

    # abstract function
    # to be defined in sub classes RedditScraper and TwitterScraper
    def runScrapper(self):
        self.message = "No Scraper defined"
        return print(self.message)

    # print the submissions
    def printSubmissions(self, a):
        #print(self.submissions, sep='\n')
        print(*a, sep='\n')



# subclass of Scraper base class, written by Yuzhe Lu, modifications by Patrick Tate
# I think it makes sense to have the reddit api variables as member variables,
# so the RedditScraper class can be differentiated from the Scraper base class.
# Needs to have all these member variables as private
class RedditScraper(Scraper):

    # *** member variables ***
    # hold pickle file of reddit submissions
    __pickledSubs: bytes
    __personalUseScript = ''
    __secret = ''
    __user_agent = '
    __username = ''
    __password = ''
    # *** member variables ***


    # default initializer takes 1 parameter
    # term =  "gaming" string variable to serach for
    # construct RedditScraper object
    def __init__(self, term_):
        # call Scraper constructor
        super().__init__(term_) #use parent search term
        # instantiate blank string to hold  pickled file
        self.__pickledSubs = ""
        self.__personalUseScript = 'Xg1TzmCGtbHcQQ'
        self.__secret = '0HnIVUpJwOAp_-R0vVwt55Js5ds'
        self.__user_agent = 'PyScraper'
        self.__username = 'Arsenal4891'
        self.__password = 'javapython'

    # returns a pickled file of reddit submissions
    # overridden function from Scraper base class
    # connect to Reddit via praw api
    # append hot_subreddit submissions to member variable submissions
    def runScrapper(self):
        print(self.getSearchTerm())

        # call reddit api using member variables
        try:
            reddit = praw.Reddit(client_id=self.__personalUseScript,
                                 client_secret=self.__secret,
                                 user_agent=self.__user_agent,
                                 username=self.__username,
                                 password=self.__password)
        except:
            print("problem loading reddit api")

        # get top 10 subreddit and hotsubreddit submissions
        subreddit = reddit.subreddit(self.getSearchTerm())
        hot_subreddit = subreddit.hot(limit=10)

        # append reddit submissions to self.submissions
        for submission in hot_subreddit:
            onesub = Post(submission.title, submission.author, submission.ups)
            self.addPost(onesub)

            # print submission
            print(submission.title, submission.id)
        self.printSubmissions(self.getSubmissions()) #prints to console the submissions found

        # send submissions to pickled file
        print("pickling submissions")
        self.__pickledSubs = pickle.dumps(self.getSubmissions())

        print("pickled submissions")

        # load pickled submissions, keeping comments here for reference
        # but moved these two lines of logic to test.py
        #print("unpickling submissions")
        #unpickled_subs = pickle.loads(self.pickleSubs)

        # return the pickled file of reddit submissions
        return self.__pickledSubs


# TwitterScraper class written by Eric Slick, modifications by Patrick Tate
class twitterScraper(Scraper):

    # *** member variables for twitter api
    __pickled_tweet_data: bytes
    __consumer_key = "fjr7cYJKLtG1Gnm6zLMrw9xXe"
    __consumer_secret_key = "96EMZVDlp7vPDUklinKPYETEln2HrAXtLTbkxry2WbYeD20DgX"
    __access_key = "1069081694982918146-V2gEiXIYK5HE05OWBI76pvjjFsoE9J"
    __access_secret = "hmxQLchOyzK6nohfqFqp2K1lfPE9ldCM5ecedACY2yhP1"
    # *** member variables for twitter api

    def __init__(self, term_):
        super().__init__(term_)
        self.__pickled_tweet_data = ""
        self.__consumer_key = "fjr7cYJKLtG1Gnm6zLMrw9xXe"
        self.__consumer_secret_key = "96EMZVDlp7vPDUklinKPYETEln2HrAXtLTbkxry2WbYeD20DgX"
        self.__access_key = "1069081694982918146-V2gEiXIYK5HE05OWBI76pvjjFsoE9J"
        self.__access_secret= "hmxQLchOyzK6nohfqFqp2K1lfPE9ldCM5ecedACY2yhP1"

    def runScrapper(self):

            auth = tweepy.OAuthHandler(self.__consumer_key, self.__consumer_secret_key)
            auth.set_access_token(self.__access_key, self.__access_secret)
            api = tweepy.API(auth)

            count = 0
            number_of_tweets = 13

            twitter_user = api.get_user(screen_name=self.getSearchTerm())
            tweets_user = api.user_timeline(screen_name=self.getSearchTerm(), tweet_mode='extended', count=number_of_tweets, include_rts=False)
            print("Printing tweets from:", twitter_user.name, "\n-------------------------------------")
            for tweet in tweets_user:
                    singleUser = twitterPost(twitter_user.name, twitter_user.screen_name, tweet.full_text, tweet.favorite_count, tweet.retweet_count)
                    self.addPost(singleUser)

            print("Pickling tweets to serialize...")
            pickled_tweet_data = pickle.dumps(self.getSubmissions())
            print("Succesfully pickled.")
            print("Unpickling tweets...")

            for post in self.getSubmissions():
                print(post.returnTweet())

            return pickled_tweet_data

