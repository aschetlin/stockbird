import logging
import os
import sys

logging.basicConfig()
logger = logging.getLogger("stockbird_logger")


def fetch_config(envvar: str, default=None) -> str:
    var = os.getenv(envvar)

    if not var:

        if default:
            var = default

        else:
            logging.error(f"You are missing {envvar}")
            sys.exit(0)

    return var


consumer_key = fetch_config("API_KEY")
consumer_secret = fetch_config("API_SECRET")
access_token = fetch_config("ACCESS_TOKEN")
access_secret = fetch_config("ACCESS_SECRET")
bearer_header = fetch_config("BEARER_HEADER")
gist_url = fetch_config("GIST_URL")
test_gist_url = fetch_config("TEST_GIST_URL")
gist_secret = fetch_config("GIST_SECRET")
log_level = fetch_config("STOCKBIRD_LOGLEVEL", default="INFO")
handle = fetch_config("STOCKBIRD_HANDLE", default="@playchess_bot")

logger.setLevel(log_level)
print(logger.level)
print(log_level)
