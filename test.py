from Scraper import RedditScraper, twitterScraper
import pickle
import tweepy



twitter = twitterScraper('realDonaldTrump')
#twitter.runScrapper()

unpickled = pickle.loads(twitter.runScrapper())
twit = ""
listo = []
for post in unpickled:
    twit = post.returnTweet()
    listo.append(twit)
    print(twit)
    #print(post.returnTweet())
    #print()
print(listo)


