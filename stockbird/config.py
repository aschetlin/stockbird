import os
import sys
import logging

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


consumer_key = fetch_config("TWT_API_KEY")
consumer_secret = fetch_config("TWT_API_SECRET")
access_token = fetch_config("TWT_ACCESS_TOKEN")
access_secret = fetch_config("TWT_ACCESS_SECRET")
gist_url = fetch_config("TWT_GIST_URL")
gist_secret = fetch_config("TWT_GIST_SECRET")
log_level = fetch_config("STOCKBIRD_LOGLEVEL", default="INFO")

logger.setLevel(log_level)
print(logger.level)
print(log_level)
