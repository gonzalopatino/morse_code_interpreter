# src/led_controller.py

import time

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    print("RPi.GPIO not available — are you running on a Raspberry Pi?")
    exit(1)

class LEDController:
    def __init__(self, red_pin: int, blue_pin: int):
        self.red_pin = red_pin
        self.blue_pin = blue_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

    def flash_dot(self):
        duration = 0.5
        print(f"⚪ DOT: RED LED ON (GPIO {self.red_pin}) for {duration}s")
        GPIO.output(self.red_pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.red_pin, GPIO.LOW)
        print(f"🔴 RED LED OFF\n")
        time.sleep(0.2)

    def flash_dash(self):
        duration = 1.5
        print(f"➖ DASH: BLUE LED ON (GPIO {self.blue_pin}) for {duration}s")
        GPIO.output(self.blue_pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.blue_pin, GPIO.LOW)
        print(f"🔵 BLUE LED OFF\n")
        time.sleep(0.2)

    def cleanup(self):
        GPIO.cleanup()
