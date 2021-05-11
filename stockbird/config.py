import os

# grab keys from environment variables
consumer_key = os.getenv("TWT_API_KEY")
consumer_secret = os.getenv("TWT_API_SECRET")
access_token = os.getenv("TWT_ACCESS_TOKEN")
access_secret = os.getenv("TWT_ACCESS_SECRET")
gist_url = os.getenv("TWT_GIST_URL")
gist_secret = os.getenv("TWT_GIST_SECRET")
