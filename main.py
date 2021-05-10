import os
import sys
import time
from collections import Counter

import tweepy
from persistqueue import Queue

consumer_key = os.getenv("TWT_API_KEY")
consumer_secret = os.getenv("TWT_API_SECRET")
access_token = os.getenv("TWT_ACCESS_TOKEN")
access_secret = os.getenv("TWT_ACCESS_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

mention_queue = Queue("queue")

try:
    with open("id.txt", "r") as idFile:
        lastId = idFile.read()

except FileNotFoundError:
    lastId = None


def update_id(id):
    with open("id.txt", "w") as idFile:
        idFile.write(id)


def __init__(args: str = None):
    if args == "cli":
        cli_access()

    get_mentions()


def get_mentions():
    global mention_queue
    global lastId

    while True:
        try:
            mentions = (
                api.mentions_timeline()
                if lastId == None
                else api.mentions_timeline(since_id=lastId)
            )

            if len(mentions) > 0:
                lastId = mentions[0].id_str

                for tweet in mentions:
                    mention_queue.put(tweet)
                    print(mention_queue.qsize())

                update_id(lastId)
                process_tweets()

        except Exception as e:
            print(e)

        time.sleep(20)


def process_tweets():
    global mention_queue

    while True:

        try:
            tweet = mention_queue.get()
            api.update_status(
                "recieved",
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True,
            )

        except Exception as e:
            print(e)

        time.sleep(5)


def cli_access():
    print("What would you like to do?\n(1) Update Status (2) DM a user\n")
    operation = int(input("> "))

    if operation == 1:
        print("What would you like to tweet? \n")
        api.update_status(input("> "))

    elif operation == 2:
        print("Who would you like to DM? \n")
        user_name = input("> ")
        user = api.get_user(user_name)

        print("What message would you like the send? \n")
        message = input("> ")
        try:
            api.send_direct_message(user.id, message)

        except tweepy.TweepError.api_code as e:
            if e.api_code == 349:
                print(
                    "You cannot message this user. "
                    "They may be private, have messages disabled, "
                    "or have your account blocked."
                )

            else:
                raise e

    else:
        print("Invalid input.")
        return


if __name__ == "__main__":
    try:
        if sys.argv:
            __init__(sys.argv[1])
        else:
            __init__()

    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
