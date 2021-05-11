import time

from stockfish import Stockfish


def handle_tweets_factory(api, tweet_queue):
    stockfish = Stockfish()

    def _():

        while True:
            print(tweet_queue.qsize())

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
                    tweet_queue.task_done()

                else:
                    stockfish.set_fen_position(substr)

                    try:
                        best_move = str(stockfish.get_best_move())
                        api.update_status(
                            f"Best move is probably: {best_move}",
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True,
                        )
                        tweet_queue.task_done()

                    except BrokenPipeError:
                        api.update_status(
                            "Invalid FEN.",
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True,
                        )
                        tweet_queue.task_done()

            except Exception as e:
                print(e)

            time.sleep(5)

    return _
