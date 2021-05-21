from stockbird.mocks.author_mock import AuthorMock


class TweetMock:
    def __init__(self, text="", author="author", id="1234"):
        self.author = AuthorMock(name=author)
        self.text = text
        self.id = id
        self.id_str = str(self.id)
