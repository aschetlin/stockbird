import time
from stockbird.config import logger

from stockbird.read_write_id import read_id, write_id


# interates through mentions, adding those that fit the criteria to tweet_queue
def get_mentions_factory(api, tweet_queue):
    def _():

        prev_id = read_id()

        while True:
            logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")

            # adds mention to list if it hasn't been processed
            mentions = (
                api.mentions_timeline()
                if prev_id == None
                else api.mentions_timeline(since_id=prev_id)
            )

            if len(mentions) > 0:
                prev_id = mentions[0].id_str

                for tweet in mentions:
                    logger.info(f"Mention from {tweet.author.name}")

                    if "fen:" in tweet.text:
                        tweet_queue.put(tweet)
                        logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")

                write_id(prev_id)

            time.sleep(20)

    return _
