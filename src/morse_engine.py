# src/morse_engine.py

import threading
import time
from enum import Enum, auto

from message_queue import MessageQueue
from led_controller import LEDController
from morse_encoder import MorseEncoder
from lcd_display import LCDDisplay


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

    def start(self):
        self.running = True
        super().start()

    def stop(self):
        self._stop_flag.set()

    def run(self):
        print("🚦 MorseEngine FSM started.")
        while self.running:
            print(f"🧠 [STATE]: {self.state.name}")   # ADD THIS LINE
            self._tick()
            time.sleep(0.1)

    def _tick(self):
        if self.state == State.IDLE:
            print("🛑 IDLE: checking for messages")
            if self.queue.has_next():
                print("✅ Message(s) available")
                self.state = State.FETCHING
            else:
                print("⏳ Queue is empty")

        elif self.state == State.FETCHING:
            self.current_message = self.queue.next_message()
            if self.current_message is None:
                self.state = State.IDLE
                return
            print(f"📥 Fetching: {self.current_message}")
            self.lcd.show_message("Sending:", self.current_message[:16])
            self.state = State.ENCODING


        elif self.state == State.ENCODING:
            encoded = self.encoder.encode(self.current_message)  # ['....', '.', '.-..', ...]
            self.morse_sequence = "".join(self.encoder.encode(self.current_message))
            print(f"🔠 Morse (flat): {self.morse_sequence}")

            self.state = State.PLAYING

        elif self.state == State.PLAYING:
            for symbol in self.morse_sequence:
                if self._stop_flag.is_set():
                    return
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
            self.queue.next_message()
            self.state = State.IDLE
