# src/led_controller.py

import time

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    from unittest import mock
    GPIO = mock.MagicMock()

class LEDController:
    def __init__(self, red_pin: int, blue_pin: int):
        self.red_pin = red_pin
        self.blue_pin = blue_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

    def flash_dot(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        time.sleep(0.5)  # 500ms
        GPIO.output(self.red_pin, GPIO.LOW)
        time.sleep(0.2)  # brief gap

    def flash_dash(self):
        GPIO.output(self.blue_pin, GPIO.HIGH)
        time.sleep(1.5)  # 1500ms
        GPIO.output(self.blue_pin, GPIO.LOW)
        time.sleep(0.2)

    def cleanup(self):
        GPIO.cleanup()
