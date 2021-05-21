from stockfish import Stockfish

from stockbird.config import test_gist_url
from stockbird.get_mentions import get_mentions
from stockbird.handle_tweets import handle_tweets
from stockbird.mocks.api_mock import TwitterAPIMock
from stockbird.mocks.tweet_mock import TweetMock
from stockbird.protos.mentions_pb2 import Mention, CommandType


def handle_tweets_helper(
    string: str, input_queue, output_queue, command=CommandType.BEST_MOVE
):
    api = TwitterAPIMock(queue=output_queue)
    tweet = TweetMock(string)
    stockfish = Stockfish()

    mention_object = Mention(
        author=tweet.author.name,
        text=tweet.text,
        id=tweet.id,
        command=command,
    )

    input_queue.put(mention_object)
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
