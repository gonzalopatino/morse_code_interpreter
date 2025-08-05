# src/message_queue.py

from queue import Queue

class MessageQueue:
    def __init__(self):
        self._queue = Queue()
        self._skip_next = False  # Flag for skipping the next message

    def add_message(self, message: str):
        self._queue.put(message)

    def next_message(self):
        if self._queue.empty():
            return None
        return self._queue.get()

    def has_messages(self):
        return not self._queue.empty()

    def size(self):
        return self._queue.qsize()

    def skip_next(self):
        print("⏭️ Skip flag set. Next message will be skipped.")
        self._skip_next = True

    def should_skip(self):
        return self._skip_next

    def clear_skip_flag(self):
        self._skip_next = False
