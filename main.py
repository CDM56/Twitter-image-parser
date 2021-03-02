from __future__ import print_function
import tweepy
from tweepy.api import API
import urllib
import os
import json
import sys
import urllib.request

from credentials import *

i = 1
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
        self.n = 0
        self.m = 1

    def on_status(self, status):
        if 'media' in status.entities:
            for image in  status.entities['media']: 
                picName = str(image['id']) + ".jpg"
                link = image['media_url']
                print(link)
                filename = os.path.join(FOLDER,picName)
                urllib.request.urlretrieve(link,filename)
                #use to test
                print(status.user.screen_name)

        else: 
            print("no media_url")

        if self.n < self.m: 
            return True
        else:
            print ('tweets = '+str(self.n))
            return False

    def on_error(self, status):
        print (status)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth, MyStreamListener(),timeout=30)
myStream.filter(track= HASHTAGS)