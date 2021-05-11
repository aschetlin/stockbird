#!/usr/bin/env python3

import sys
import threading

from persistqueue import Queue
from stockfish import Stockfish
from stockbird.api import TwitterAPI
from stockbird.cli_access import cli_access
from stockbird.get_mentions import get_mentions_factory
from stockbird.handle_tweets import handle_tweets_factory


def __init__(api, tweet_queue, args: str = None):
    if args == "cli":
        cli_access(api)

    mention_getter = threading.Thread(
        target=get_mentions_factory(api, tweet_queue)
    )
    tweet_handler = threading.Thread(
        target=handle_tweets_factory(api, tweet_queue)
    )
    mention_getter.start()
    tweet_handler.start()


if __name__ == "__main__":
    api = TwitterAPI()
    stockfish = Stockfish()
    tweet_queue = Queue("queue")

    try:

        if len(sys.argv) > 1:
            __init__(
                api=api,
                tweet_queue=tweet_queue,
                stockfish=stockfish,
                args=sys.argv[1],
            )

        else:
            __init__(api=api, tweet_queue=tweet_queue, stockfish=stockfish)

    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
