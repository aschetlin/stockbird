from stockfish import Stockfish

from stockbird.handle_tweets import handle_tweets
from stockbird.get_mentions import get_mentions
from stockbird.mocks.api_mock import TwitterAPIMock
from stockbird.mocks.tweet_mock import TweetMock
from stockbird.config import test_gist_url


def handle_tweets_helper(string: str, input_queue, output_queue):
    api = TwitterAPIMock(queue=output_queue)
    tweet = TweetMock(string)
    stockfish = Stockfish()

    input_queue.put(tweet)
    handle_tweets(api, input_queue, stockfish)
    output = output_queue.get()
    output_queue.task_done()

    return output


def get_mentions_helper(text: str, output_queue):
    tweets = [
        TweetMock(
            text=text,
        ),
    ]
    api = TwitterAPIMock(output_queue, tweets=tweets)

    get_mentions(api, output_queue, gist_url=test_gist_url)

    if output_queue.qsize() > 0:
        output = output_queue.get()
        output_queue.task_done()

    else:
        output = None

    return output
