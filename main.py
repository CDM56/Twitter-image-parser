import tweepy
from tweepy.api import API
import os
import urllib.request

from credentials import *

consumer_key = GIT_CKEY
consumer_secret = GIT_CKEY_S
access_token = GIT_ACCESS
access_token_secret = GIT_ACCESS_S
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        self.api = api or API()

    def on_status(self, status):
        try:
            if 'media' in status.entities: # If a media is present in the tweet
                for image in  status.entities['media']: 
                    picName = str(image['id']) + ".jpg" # Image naming. Naming by id to remove double the same image (retweets)
                    link = image['media_url'] + ":orig"
                    print(link) # Print the tweet media link for debug
                    filename = os.path.join(FOLDER,picName)
                    urllib.request.urlretrieve(link,filename) #Writing the image in the folder given in credentials.py
                    #use to test
                    print(status.user.screen_name) # Print twwet username for debug

            else: 
                print("no media_url") # if no media, for debug
            return True # for program loop

        except:
            return True

    def on_error(self, status):
        print (status)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth, MyStreamListener(),timeout=30) # watch tweet stream with packet timeout of 30 seconds
myStream.filter(track= HASHTAGS)