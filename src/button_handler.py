# src/button_handler.py

import RPi.GPIO as GPIO
import time

class ButtonHandler:
    def __init__(self, button_pin: int, callback=None, bouncetime_ms: int = 500):
        self.button_pin = button_pin
        self.callback = callback

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Attach the interrupt
        GPIO.add_event_detect(
            self.button_pin,
            GPIO.RISING,
            callback=self._internal_callback,
            bouncetime=bouncetime_ms
        )

    def _internal_callback(self, channel):
        print("🔘 Button pressed on GPIO", self.button_pin)
        if self.callback:
            self.callback()

    def cleanup(self):
        GPIO.cleanup()
