from led_controller import LEDController      # correct after install
import time

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
