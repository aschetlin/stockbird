import os
import sys

import pytest
from persistqueue import Queue

sys.path.append(os.path.join(os.path.dirname(__file__), "helpers"))


def new_queue(queue_name):
    queue = Queue(".queues/" + queue_name)

    while queue.qsize():
        queue.get()
        queue.task_done()

    return queue


@pytest.fixture
def input_queue():
    return new_queue("test_input_queue")


@pytest.fixture
def output_queue():
    return new_queue("test_output_queue")
