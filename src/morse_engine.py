# src/morse_engine.py

import threading
import time
from enum import Enum, auto

from src.message_queue import MessageQueue
from src.led_controller import LEDController
from src.morse_encoder import MorseEncoder
from src.lcd_display import LCDDisplay
from threading import Event


class State(Enum):
    IDLE = auto()
    FETCHING = auto()
    ENCODING = auto()
    PLAYING = auto()
    ADVANCING = auto()


class MorseEngine(threading.Thread):
    def __init__(self, led_controller: LEDController, message_queue: MessageQueue, lcd_display: LCDDisplay):
        super().__init__(daemon=True)
        self.leds = led_controller
        self.queue = message_queue
        self.lcd = lcd_display
        self.encoder = MorseEncoder()
        self._stop_flag = threading.Event()
        self.state = State.IDLE
        self.current_message = ""
        self.morse_sequence = ""
        self.running = False
        self._skip_flag = Event()


    def start(self):
        self.running = True
        super().start()

    def stop(self):
        self._stop_flag.set()

    def run(self):
        print("🚦 MorseEngine FSM started.")
        while not self._stop_flag.is_set():
            print(f"🧠 [STATE]: {self.state.name}")
            if not self._tick():
                break
            time.sleep(0.1)
        print("✅ MorseEngine stopped.")

    def _tick(self):
        if self.state == State.IDLE:
            print("🛑 IDLE: checking for messages")
            if self.queue.has_messages():
                print("✅ Message(s) available")
                self.state = State.FETCHING
            else:
                print("⏳ Queue is empty")

        elif self.state == State.FETCHING:
            self.current_message = self.queue.next_message()
            if self.current_message is None:
                self.state = State.IDLE
                return True
            print(f"📥 Fetching: {self.current_message}")
            self.lcd.show_message("Sending:", self.current_message[:16])
            self.state = State.ENCODING

        elif self.state == State.ENCODING:
            encoded = self.encoder.encode(self.current_message)
            print(f"🔠 Morse: {encoded}")
            self.morse_sequence = "".join(encoded)
            print(f"🔠 Morse (flat): {self.morse_sequence}")
            self.state = State.PLAYING

        elif self.state == State.PLAYING:
            for symbol in self._flatten_morse(self.morse_sequence):
                if self._stop_flag.is_set():
                    print("🛑 Stop flag detected during PLAYING")
                    return False  # Exit thread
                if self._skip_flag.is_set():
                    print("⏩ Skipping current message...")
                    self._skip_flag.clear()
                    break
                if symbol == ".":
                    self.leds.flash_dot()
                elif symbol == "-":
                    self.leds.flash_dash()
                elif symbol == "/":
                    time.sleep(1.0)
                else:
                    time.sleep(0.5)
            self.state = State.ADVANCING

        elif self.state == State.ADVANCING:
            print("➡️ Advancing to next message")
            if self.queue.should_skip():
                skipped = self.queue.next_message()
                print(f"⏩ Skipping message: {skipped}")
                self.queue.clear_skip_flag()
            self.state = State.IDLE

        return True  # Continue loop

 

    def request_skip(self):
        print("⏭️ Skip requested via button press")
        self._skip_flag.set()

    def _flatten_morse(self, morse_sequence: list[str]) -> str:
        return ''.join(morse_sequence)

    def _sleep_interruptible(self, duration):
        """Sleep in small chunks to allow fast shutdown."""
        elapsed = 0
        interval = 0.05  # 50ms
        while elapsed < duration:
            if self._stop_flag.is_set():
                break
            time.sleep(interval)
            elapsed += interval



