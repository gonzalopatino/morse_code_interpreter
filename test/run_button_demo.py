
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.button_handler import ButtonHandler


# This is the function that will run when the button is pressed
def on_button_press():
    print("✅ Callback: Button was pressed!")

button = ButtonHandler(button_pin=18, callback=on_button_press)

try:
    print("🟢 Waiting for button press... (CTRL+C to exit)")
    while True:
        time.sleep(0.1)  # keep CPU idle
except KeyboardInterrupt:
    print("🛑 Exiting test...")
finally:
    button.cleanup()
