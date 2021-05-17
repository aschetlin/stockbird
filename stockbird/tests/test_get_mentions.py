from stockbird.tests.helpers.utils import get_mentions_helper


def test_get_mentions_valid(output_queue):
    output = get_mentions_helper(
        text="""
        @stockbirdchess
        fen:rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 2 4
        """,
        output_queue=output_queue,
    )

    assert output


def test_get_mentions_invalid(output_queue):
    output = get_mentions_helper(
        text="@stockbirdchess foobar",
        output_queue=output_queue,
    )

    assert not output
