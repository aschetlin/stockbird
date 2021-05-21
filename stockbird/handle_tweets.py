import redis

from stockbird.command_resources import CommandResources
from stockbird.commands import commands
from stockbird.config import logger
from stockbird.protos.mentions_pb2 import CommandType


def handle_tweets(
    api,
    tweet_queue,
    stockfish,
    r=redis.Redis(host="localhost", port=6379, db=0),
):

    logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")

    try:
        tweet = tweet_queue.get()
        command = commands[CommandType.Name(tweet.command)]
        command(CommandResources(api, tweet, stockfish, r))

    finally:
        tweet_queue.task_done()
        logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")


def handle_tweets_factory(api, tweet_queue, stockfish):
    def _():

        while True:
            handle_tweets(api, tweet_queue, stockfish)

    return _
