import chess

from stockbird.config import logger


def handle_tweets(api, tweet_queue, stockfish):
    logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")

    try:
        tweet = tweet_queue.get()

        index = tweet.text.index("fen:") + 4
        substr = tweet.text[index:]

        if "fen:" in substr:
            api.update_status(
                "Your tweet contained multiple FEN keywords.",
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True,
            )

        else:

            try:
                board = chess.Board(fen=substr)
                stockfish.set_fen_position(board.fen())
                best_move = stockfish.get_best_move()
                api.update_status(
                    f"Best move is probably: {best_move}",
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True,
                )

            except ValueError:
                api.update_status(
                    "Invalid FEN.",
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True,
                )

    finally:
        tweet_queue.task_done()
        logger.debug(f"Tweet Queue: {tweet_queue.qsize()}")


def handle_tweets_factory(api, tweet_queue, stockfish):
    def _():

        while True:
            handle_tweets(api, tweet_queue, stockfish)

    return _
