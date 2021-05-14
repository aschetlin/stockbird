class TwitterAPIMock:
    def __init__(self, queue):
        self.queue = queue

    def update_status(
        self, status, *, in_reply_to_status_id, auto_populate_reply_metadata
    ):
        self.queue.put(status)
