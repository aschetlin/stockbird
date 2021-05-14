# create auth & api objects
import tweepy

from stockbird.config import (
    access_secret,
    access_token,
    consumer_key,
    consumer_secret,
)


class TwitterAPI:
    def __init__(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        self.api = tweepy.API(auth)
