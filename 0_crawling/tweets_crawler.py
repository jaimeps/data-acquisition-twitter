
import tweepy
import json
import time
import csv
import os


CONSUMER_KEY = 'yours'
CONSUMER_SECRET = 'yours'
ACCESS_TOKEN = 'yours'
ACCESS_TOKEN_SECRET = 'yours'


BUZZWORDS = ["football", "49ers", "longhorns", "sports", "win", "lose"]

# individual Bay Area locations
LOCATIONS = {"San Francisco": [-122.75,36.8,-121.75,37.8],
             "East Bay": [37.781133, -122.318459,37.888608, -122.215505],
             "South Bay": [37.627164, -122.488075,37.730253, -122.364656],
             "San Jose": [37.212669, -122.013394,37.440182, -121.817675],
             "Palo Alto": [37.331512, -122.263348,37.554304, -121.955228]}

# pretty much the whole Bay Area
LOC = [37.168867, -122.598694, 38.026034, -121.638724]


class MSAN692GP(tweepy.StreamListener):

    def __init__(self):

        super(MSAN692GP, self).__init__()
        self.twts = 0
    def on_data(self, data):

        try:

            with open("YOUR_FILE_PATH/NAME_OF_FILE.json", "a") as outFile:
                outFile.write(data)
                self.twts += 1
                if self.twts < 500:
                    return True
                else:
                    return False
        except BaseException, e:
            print 'failed on data', str(e)
            time.sleep(5)

    def on_error(self, status):

        print status


start = time.time()
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweets = tweepy.Stream(auth, MSAN692GP())
tweets.filter(track=BUZZWORDS, locations=LOCATIONS["San Francisco"])
end = time.time()

print end - start











