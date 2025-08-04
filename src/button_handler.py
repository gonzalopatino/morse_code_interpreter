# src/button_handler.py

import RPi.GPIO as GPIO

class ButtonHandler:
    def __init__(self, button_pin: int, callback=None, bouncetime_ms: int = 300):
        self.button_pin = button_pin
        self.callback = callback

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN)  # External pull-up, no internal resistor

        # Defensive: remove previous detect if it exists
        try:
            GPIO.remove_event_detect(self.button_pin)
        except RuntimeError:
            pass

        # Register falling edge for external pull-up
        GPIO.add_event_detect(
            self.button_pin,
            GPIO.FALLING,  # ✅ Falling edge = button press
            callback=self._internal_callback,
            bouncetime=bouncetime_ms
        )

    def _internal_callback(self, channel):
        print(f"🔘 Button pressed on GPIO {self.button_pin}")
        if self.callback:
            self.callback()

    def cleanup(self):
        GPIO.cleanup(self.button_pin)
