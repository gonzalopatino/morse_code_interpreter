from button_handler import ButtonHandler
import time

# Callback function triggered on button press
def on_button_press():
    print("✅ Callback: Button was pressed!")

# Initialize ButtonHandler on GPIO 18
button = ButtonHandler(button_pin=18, callback=on_button_press)

try:
    print("🟢 Waiting for button press... (CTRL+C to exit)")
    while True:
        time.sleep(0.1)  # Prevents CPU hogging
except KeyboardInterrupt:
    print("🛑 Exiting test...")
finally:
    button.cleanup()
