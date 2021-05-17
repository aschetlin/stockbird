import time

from stockbird.config import logger
from stockbird.read_write_id import read_id, write_id


def get_mentions(api, tweet_queue):
    prev_id = read_id()

    logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")

    mentions = (
        api.mentions_timeline(since_id=prev_id)
        if prev_id
        else api.mentions_timeline()
    )

    if len(mentions) > 0:
        prev_id = mentions[0].id_str

        for tweet in mentions:

            logger.info(f"Mention from {tweet.author.name}")

            if "fen:" in tweet.text:
                tweet_queue.put(tweet)
                logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")

        write_id(prev_id)


def get_mentions_factory(api, tweet_queue):
    def _():
        while True:
            get_mentions(api, tweet_queue)
            time.sleep(20)

    return _
