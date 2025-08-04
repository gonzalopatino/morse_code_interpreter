# test/test_queue.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from message_queue import MessageQueue

def test_message_queue():
    q = MessageQueue()

    q.add_message("HELLO")
    q.add_message("WORLD")
    q.add_message("SOS")

    print("➡️ Getting first message:", q.next_message())  # HELLO
    print("👀 Peeking current:", q.peek_current())        # HELLO

    print("➡️ Getting second message:", q.next_message()) # WORLD
    print("➡️ Getting third message:", q.next_message())  # SOS
    print("➡️ Getting next (should be None):", q.next_message())  # None

    print("🧹 Clearing queue")
    q.clear()
    print("✅ Queue cleared. Current:", q.peek_current(), "Has next:", q.has_next())

if __name__ == "__main__":
    test_message_queue()
