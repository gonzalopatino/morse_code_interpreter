# src/message_queue.py

from collections import deque

class MessageQueue:
    def __init__(self):
        self._queue = deque()
        self._current = None

    def add_message(self, message: str):
        self._queue.append(message)

    def peek_current(self) -> str | None:
        # Peek at the front of the queue (don't remove it)
        if self._queue:
            return self._queue[0]
        return None

    def next_message(self) -> str | None:
        # Move to next message and store it as current
        if self._queue:
            self._current = self._queue.popleft()
        else:
            self._current = None
        return self._current

    def has_next(self) -> bool:
        return bool(self._queue)

    def clear(self):
        self._queue.clear()
        self._current = None

    def size(self) -> int:
        return len(self._queue)
