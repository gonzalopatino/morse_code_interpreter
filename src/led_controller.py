import time
import threading
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.constants import DOT_DURATION, DASH_DURATION, INTRA_CHAR_GAP

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    print("RPi.GPIO not available — are you running on a Raspberry Pi?")
    exit(1)


class LEDController:
    def __init__(self, red_pin: int, blue_pin: int, stop_flag: threading.Event = None):
        self.red_pin = red_pin
        self.blue_pin = blue_pin
        self.stop_flag = stop_flag or threading.Event()  # Optional, defaults to unset

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

    def flash_dot(self):
        print(f"⚪ DOT: RED LED ON (GPIO {self.red_pin}) for {DOT_DURATION}s")
        GPIO.output(self.red_pin, GPIO.HIGH)
        self._sleep_interruptible(DOT_DURATION)
        GPIO.output(self.red_pin, GPIO.LOW)
        print("🔴 RED LED OFF\n")
        self._sleep_interruptible(INTRA_CHAR_GAP)

    def flash_dash(self):
        print(f"➖ DASH: BLUE LED ON (GPIO {self.blue_pin}) for {DASH_DURATION}s")
        GPIO.output(self.blue_pin, GPIO.HIGH)
        self._sleep_interruptible(DASH_DURATION)
        GPIO.output(self.blue_pin, GPIO.LOW)
        print("🔵 BLUE LED OFF\n")
        self._sleep_interruptible(INTRA_CHAR_GAP)

    def _sleep_interruptible(self, duration):
        """Breaks sleep into 50ms intervals and checks for stop signal."""
        end_time = time.time() + duration
        while time.time() < end_time:
            if self.stop_flag.is_set():
                break
            time.sleep(0.05)

    def cleanup(self):
        GPIO.cleanup()
