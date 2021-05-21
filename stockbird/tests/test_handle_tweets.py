from stockbird.protos.mentions_pb2 import CommandType
from stockbird.tests.helpers.utils import handle_tweets_helper


def test_valid_best_move(input_queue, output_queue):
    output = handle_tweets_helper(
        """
        @stockbirdchess
        fen:rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 2 4
        """,
        input_queue,
        output_queue,
    )
    assert "Best move is probably: " in output


def test_valid_start_game(input_queue, output_queue):
    output = handle_tweets_helper(
        "@playchess_bot start game",
        input_queue,
        output_queue,
        command=CommandType.START_GAME,
    )

    assert "New game started." in output


def test_duplicate_game(input_queue, output_queue):
    output = handle_tweets_helper(
        "playchess_bot start game",
        input_queue,
        output_queue,
        author="duplicate_guy",
        command=CommandType.START_GAME,
    )

    assert "You already have an in-progress game." in output


def test_invalid_fen(input_queue, output_queue):
    output = handle_tweets_helper(
        """
        @stockbirdchess
        fen:fjaklsdfjkaldsjfklasdjfkladsjfkldsajfksa
        """,
        input_queue,
        output_queue,
    )
    assert output == "Invalid FEN."


def test_multiple_fen(input_queue, output_queue):
    output = handle_tweets_helper(
        """
        @stockbirdchess fen:537453480 fen:584035894
        """,
        input_queue,
        output_queue,
    )
    assert output == "Your tweet contained multiple FEN keywords."
