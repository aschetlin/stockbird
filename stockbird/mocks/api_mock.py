from typing import List

from stockbird.mocks.tweet_mock import TweetMock


class TwitterAPIMock:
    def __init__(self, queue, tweets: List[TweetMock] = None):
        self.queue = queue
        self.tweets = tweets

    def update_status(
        self, status, *, in_reply_to_status_id, auto_populate_reply_metadata
    ):
        self.reply_id = in_reply_to_status_id
        self.reply_metadata = auto_populate_reply_metadata
        self.queue.put(status)

    def mentions_timeline(self, since_id=None):
        self.since_id = since_id
        return self.tweets
