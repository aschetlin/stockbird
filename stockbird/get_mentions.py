import time

from stockbird.read_write_id import read_id, write_id
from stockbird.handle_tweets import handle_tweets


# interates through mentions, adding those that fit the criteria to tweet_queue
def get_mentions_factory(api, tweet_queue):
    def _():

        prev_id = read_id()

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

                    write_id(prev_id)
                    handle_tweets()

            except Exception as e:
                print(e)

            time.sleep(20)

    return _
