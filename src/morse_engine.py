import threading
import time
from enum import Enum, auto

from src.constants import DOT_DURATION, DASH_DURATION, INTRA_CHAR_GAP, INTER_LETTER_GAP, INTER_WORD_GAP
from src.message_queue import MessageQueue
from src.led_controller import LEDController
from src.morse_encoder import MorseEncoder
from src.lcd_display import LCDDisplay


class State(Enum):
    IDLE = auto()
    FETCHING = auto()
    ENCODING = auto()
    PLAYING = auto()
    ADVANCING = auto()


class MorseEngine(threading.Thread):
    """
    A threaded finite state machine (FSM) to drive LED Morse code playback
    with message skipping via button and status display on an LCD.
    """

    def __init__(self, led_controller: LEDController, message_queue: MessageQueue, lcd_display: LCDDisplay):
        super().__init__(daemon=True)
        self.leds = led_controller
        self.queue = message_queue
        self.lcd = lcd_display
        self.encoder = MorseEncoder()
        self._stop_flag = threading.Event()
        self._skip_flag = threading.Event()
        self.state = State.IDLE
        self.current_message = ""
        self.morse_sequence = ""

    def start(self):
        print("🚦 MorseEngine FSM started.")
        super().start()

    def stop(self):
        print("🛑 Stopping MorseEngine...")
        self._stop_flag.set()

    def run(self):
        while not self._stop_flag.is_set():
            print(f"🧠 [STATE]: {self.state.name}")
            self._tick()
            time.sleep(0.1)
        print("✅ MorseEngine stopped.")

    def _tick(self):
        if self.state == State.IDLE:
            self._handle_idle()

        elif self.state == State.FETCHING:
            self._handle_fetching()

        elif self.state == State.ENCODING:
            self._handle_encoding()

        elif self.state == State.PLAYING:
            self._handle_playing()

        elif self.state == State.ADVANCING:
            self._handle_advancing()

    def _handle_idle(self):
        print("🛑 IDLE: checking for messages")
        if self.queue.has_messages():
            print("✅ Message(s) available")
            self.state = State.FETCHING
        else:
            print("⏳ Queue is empty")

    def _handle_fetching(self):
        self.current_message = self.queue.next_message()
        if self.current_message:
            print(f"📥 Fetching: {self.current_message}")
            self.lcd.show_message("Sending:", self.current_message[:16])
            self.state = State.ENCODING
        else:
            self.state = State.IDLE

    def _handle_encoding(self):
        encoded = self.encoder.encode(self.current_message)
        print(f"🔠 Morse: {encoded}")
        self.morse_sequence = ''.join(encoded)
        print(f"🔠 Morse (flat): {self.morse_sequence}")
        self.state = State.PLAYING

    def _handle_playing(self):
        for symbol in self._flatten_morse(self.morse_sequence):
            if self._stop_flag.is_set():
                print("🛑 Stop flag detected during PLAYING")
                return

            if self._skip_flag.is_set():
                print("⏩ Skipping current message...")
                self._skip_flag.clear()
                break

            if symbol == ".":
                self.leds.flash_dot()
                self._sleep_interruptible(INTRA_CHAR_GAP)
            elif symbol == "-":
                self.leds.flash_dash()
                self._sleep_interruptible(INTRA_CHAR_GAP)
            elif symbol == "/":
                self._sleep_interruptible(INTER_WORD_GAP)
            else:
                self._sleep_interruptible(INTER_LETTER_GAP)

        self.state = State.ADVANCING

    def _handle_advancing(self):
        print("➡️ Advancing to next message")
        if self.queue.should_skip():
            skipped = self.queue.next_message()
            print(f"⏩ Skipping message: {skipped}")
            self.queue.clear_skip_flag()
        self.state = State.IDLE

    def request_skip(self):
        print("⏭️ Skip requested via button press")
        self._skip_flag.set()

    def _flatten_morse(self, morse_sequence: list[str]) -> str:
        return ''.join(morse_sequence)

    def _sleep_interruptible(self, duration):
        interval = 0.05
        end_time = time.time() + duration
        while time.time() < end_time:
            if self._stop_flag.is_set():
                break
            time.sleep(interval)
