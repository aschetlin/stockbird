import threading

from persistqueue import Queue
from stockbird.handle_tweets import handle_tweets_factory
from stockbird.mocks.api_mock import TwitterAPIMock
from stockbird.mocks.tweet_mock import TweetMock


def handle_tweets_helper(string: str, input_queue, output_queue):
    api = TwitterAPIMock(output_queue)
    tweet = TweetMock(string)

    thread = threading.Thread(
        target=handle_tweets_factory(api, input_queue)
    )

    thread.start()

    input_queue.put(tweet)
    output = output_queue.get()
    output_queue.task_done()
    input_queue.put(None)

    thread.join()

    return output
