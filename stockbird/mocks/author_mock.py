class AuthorMock:
    def __init__(self, name: str = "author") -> None:
        self.author = name

    def name(self):
        return self.author
