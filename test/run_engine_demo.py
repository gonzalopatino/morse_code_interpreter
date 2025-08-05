# test/run_engine_demo.py

import os
import sys
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from led_controller import LEDController
from message_queue import MessageQueue
from lcd_display import LCDDisplay
from morse_engine import MorseEngine

# Initialize components
leds = LEDController(red_pin=23, blue_pin=24)
queue = MessageQueue()
lcd = LCDDisplay()
engine = MorseEngine(leds, queue, lcd)

try:
    # Preload a few test messages
    queue.add_message("HELLO")
    queue.add_message("WORLD")
    queue.add_message("SOS")
    print("📦 Queue size:", queue.size())



    engine.start()

    print("📡 MorseEngine is running (CTRL+C to stop)...")
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n🛑 Stopping MorseEngine...")
    engine.stop()
    engine.join()
finally:
    leds.cleanup()
    lcd.cleanup()
    print("🧹 Cleaned up GPIO and LCD")
