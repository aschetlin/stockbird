import re
import time

from stockbird.config import gist_url, handle, logger
from stockbird.exceptions import InvalidCommandException
from stockbird.protos.mentions_pb2 import CommandType, Mention
from stockbird.read_write_id import read_id, write_id

commands = {
    "fen": CommandType.BEST_MOVE,
    "start": CommandType.START_GAME,
}


def get_mentions(api, tweet_queue, gist_url=gist_url):
    prev_id = read_id(url=gist_url)

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

            regex = r"\b([\w_]+): ?(.*)"
            match_data = re.search(regex, tweet.text)

            if not match_data:
                logger.warning(f"Invalid command attempted: {tweet.text}")
                continue

            command_str = match_data.group(1)

            if command_str not in commands:
                logger.warning(f"Invalid command attempted: {tweet.text}")
                continue

            command = commands[command_str]

            message_object = Mention(
                author=tweet.author.name,
                text=tweet.text,
                id=str(tweet.id),
                command=command,
            )

            tweet_queue.put(message_object)
            logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")

        write_id(prev_id, url=gist_url)


def get_mentions_factory(api, tweet_queue):
    def _():
        while True:
            get_mentions(api, tweet_queue)
            time.sleep(20)

    return _
