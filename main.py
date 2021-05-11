#!/usr/bin/env python3

import os
import sys
import time
from collections import Counter

import tweepy
from persistqueue import Queue
from stockfish import Stockfish

# grab keys from environment variables
consumer_key = os.getenv("TWT_API_KEY")
consumer_secret = os.getenv("TWT_API_SECRET")
access_token = os.getenv("TWT_ACCESS_TOKEN")
access_secret = os.getenv("TWT_ACCESS_SECRET")

# create auth & api objects
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# create stockfish object
stockfish = Stockfish()

# create empty queue
tweet_queue = Queue("queue")


# persists prev_id to avoid reprocessing mentions
try:
    with open("id.txt", "r") as idfile:
        prev_id = idfile.read()

except FileNotFoundError:
    prev_id = None


def update_id(id):
    with open("id.txt", "w") as idfile:
        idfile.write(id)


def __init__(args: str = None):
    if args == "cli":
        cli_access()

    get_mentions()


# interates through mentions, adding those that fit the criteria to tweet_queue
def get_mentions():
    global tweet_queue
    global prev_id

    while True:
        print(tweet_queue.qsize())
        try:
            # adds mention to list if it hasn't been processed
            mentions = (
                api.mentions_timeline()
                if prev_id == None
                else api.mentions_timeline(since_id=prev_id)
            )

            if len(mentions) > 0:
                prev_id = mentions[0].id_str

                for tweet in mentions:
                    print(f"Mention from {tweet.author.name}")

                    if "fen:" in tweet.text:
                        tweet_queue.put(tweet)
                        print(tweet_queue.qsize())

                update_id(prev_id)
                handle_tweets()

        except Exception as e:
            print(e)

        time.sleep(20)


def handle_tweets():
    global tweet_queue

    while True:
        print(tweet_queue.qsize())

        try:
            tweet = tweet_queue.get()
            index = tweet.text.index("fen:") + 4
            substr = tweet.text[index:]

            if "fen:" in substr:
                api.update_status(
                    "Your tweet contained multiple FEN keywords.",
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True,
                )
                tweet_queue.task_done()

            else:
                stockfish.set_fen_position(substr)

                try:
                    best_move = str(stockfish.get_best_move())
                    api.update_status(
                        f"Best move is probably: {best_move}",
                        in_reply_to_status_id=tweet.id,
                        auto_populate_reply_metadata=True,
                    )
                    tweet_queue.task_done()

                except BrokenPipeError:
                    api.update_status(
                        "Invalid FEN.",
                        in_reply_to_status_id=tweet.id,
                        auto_populate_reply_metadata=True,
                    )
                    tweet_queue.task_done()

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
        try:
            __init__(sys.argv[1])
        except IndexError:
            __init__()

    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
