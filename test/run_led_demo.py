import sys
import os
import time

# ✅ Fix: Add parent directory to import path BEFORE importing from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.led_controller import LEDController  # this works now

led = LEDController(red_pin=23, blue_pin=24)

try:
    print("🔴 Flashing DOT")
    led.flash_dot()
    time.sleep(1)

    print("🔵 Flashing DASH")
    led.flash_dash()
    time.sleep(1)

    print("✅ Hardware LED test complete")

finally:
    led.cleanup()
