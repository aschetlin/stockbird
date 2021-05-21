import requests
from stockbird.config import bearer_header


def get_conversation_id(id):
    uri = "https://api.twitter.com/2/tweets?"
    header = {"Authorization": f"Bearer {bearer_header}"}

    params = {"ids": id, "tweet.fields": "conversation_id"}

    resp = requests.get(uri, headers=header, params=params)
    return resp.json()["data"][0]["conversation_id"]
