from stockbird.protos.mentions_pb2 import CommandType
from stockbird.tests.helpers.utils import get_mentions_helper


def test_invalid(output_queue):
    output = get_mentions_helper(
        text="foobar",
        output_queue=output_queue,
    )

    assert not output


def test_best_move_valid(output_queue):
    output = get_mentions_helper(
        text="""
        fen:rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 2 4
        """,
        output_queue=output_queue,
    )

    assert output.command == CommandType.BEST_MOVE


def test_start_game_valid(output_queue):
    output = get_mentions_helper(
        text="start game", output_queue=output_queue
    )

    assert output.command == CommandType.START_GAME
