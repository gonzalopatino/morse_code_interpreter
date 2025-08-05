# test/run_engine_demo.py

import os
import sys
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.button_handler import ButtonHandler
from src.led_controller import LEDController
from src.message_queue import MessageQueue
from src.lcd_display import LCDDisplay
from src.morse_engine import MorseEngine

# Initialize components
leds = LEDController(red_pin=23, blue_pin=24)
queue = MessageQueue()
lcd = LCDDisplay()
button = ButtonHandler(button_pin=18, callback=lambda: queue.skip_to_next())
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
    button.cleanup()
    leds.cleanup()
    lcd.cleanup()
    print("🧹 Cleaned up GPIO, LCD, and button")

