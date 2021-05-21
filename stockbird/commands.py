import random

import chess
import redis

from stockbird.command_resources import CommandResources
from stockbird.protos.mentions_pb2 import CommandType


def best_move(resources: CommandResources):
    api = resources.api
    stockfish = resources.stockfish
    tweet = resources.tweet

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
            # Throws ValueError if FEN is invalid
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


def start_game(resources: CommandResources):
    api = resources.api
    r = resources.redis
    stockfish = resources.stockfish
    tweet = resources.tweet

    current_fen = r.get(tweet.author)
    if current_fen:
        api.update_status(
            f"You already have an in-progress game.",
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True,
        )
        return

    color = random.choice(("black", "white"))

    if color == "black":
        board = chess.Board()
        stockfish.set_fen_position(board.fen())
        move = stockfish.get_best_move()

        if move:
            board.push_san(move)
            r.set(tweet.author, board.fen())

        else:
            raise Exception("Stockfish did not return a move.")

        api.update_status(
            f"""New game started. You will play black.
            I play {move}.""",
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True,
        )

    else:
        board = chess.Board()
        r.set(tweet.author, board.fen())

        api.update_status(
            f"New game started. You will play white.",
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True,
        )


commands = dict(zip(CommandType.keys(), [best_move, start_game]))
