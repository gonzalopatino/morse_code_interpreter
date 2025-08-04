import unittest
from unittest.mock import patch, MagicMock
from src.led_controller import LEDController

class TestLEDController(unittest.TestCase):
    @patch("src.led_controller.GPIO")
    @patch("src.led_controller.time.sleep", return_value=None)  # skip delays
    def test_flash_dot(self, mock_sleep, mock_gpio):
        led = LEDController(red_pin=17, blue_pin=27)
        led.flash_dot()

        # Ensure correct GPIO pin turned ON then OFF
        mock_gpio.output.assert_any_call(17, mock_gpio.HIGH)
        mock_gpio.output.assert_any_call(17, mock_gpio.LOW)

        # Ensure correct timing (0.5s + 0.2s = 2 calls)
        self.assertEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_any_call(0.5)
        mock_sleep.assert_any_call(0.2)

    @patch("src.led_controller.GPIO")
    @patch("src.led_controller.time.sleep", return_value=None)
    def test_flash_dash(self, mock_sleep, mock_gpio):
        led = LEDController(red_pin=17, blue_pin=27)
        led.flash_dash()

        mock_gpio.output.assert_any_call(27, mock_gpio.HIGH)
        mock_gpio.output.assert_any_call(27, mock_gpio.LOW)

        self.assertEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_any_call(1.5)
        mock_sleep.assert_any_call(0.2)

if __name__ == "__main__":
    unittest.main()
