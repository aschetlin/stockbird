import requests

from stockbird.config import gist_secret, gist_url


def read_id(url=gist_url):

    with requests.get(
        f"https://api.github.com/gists/{url}",
        headers={"Accept": "application/vnd.github.v3+json"},
    ) as r:

        return (
            r.json()
            .get("files", {"prod-id.txt": {"content": None}})
            .get("prod-id.txt", {"content": None})
            .get("content", None)
        )


def write_id(id, url=gist_url):
    requests.patch(
        f"https://api.github.com/gists/{url}",
        headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {gist_secret}",
        },
        json={"files": {"prod-id.txt": {"content": id}}},
    )
