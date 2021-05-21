from stockbird.protos.mentions_pb2 import CommandType
import chess

from stockbird.config import logger
from stockbird.commands import commands


def handle_tweets(api, tweet_queue, stockfish):
    logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")

    try:
        tweet = tweet_queue.get()
        command = commands[CommandType.Name(tweet.command)]
        command(api, tweet, stockfish)

    finally:
        tweet_queue.task_done()
        logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")


def handle_tweets_factory(api, tweet_queue, stockfish):
    def _():

        while True:
            handle_tweets(api, tweet_queue, stockfish)

    return _
