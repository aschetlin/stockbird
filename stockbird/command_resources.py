class CommandResources:
    def __init__(self, api, tweet, stockfish, redis) -> None:
        self.api = api
        self.tweet = tweet
        self.stockfish = stockfish
        self.redis = redis
