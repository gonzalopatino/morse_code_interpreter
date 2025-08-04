# src/lcd_display.py

import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

class LCDDisplay:
    def __init__(self):
        self.lcd_columns = 16
        self.lcd_rows = 2

        self.lcd_rs = digitalio.DigitalInOut(board.D17)
        self.lcd_en = digitalio.DigitalInOut(board.D27)
        self.lcd_d4 = digitalio.DigitalInOut(board.D5)
        self.lcd_d5 = digitalio.DigitalInOut(board.D6)
        self.lcd_d6 = digitalio.DigitalInOut(board.D13)
        self.lcd_d7 = digitalio.DigitalInOut(board.D26)

        self.lcd = characterlcd.Character_LCD_Mono(
            self.lcd_rs, self.lcd_en,
            self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7,
            self.lcd_columns, self.lcd_rows
        )
        self.clear()

    def show_message(self, line1: str, line2: str = ""):
        message = f"{line1[:16]}\n{line2[:16]}"
        self.lcd.message = message

    def clear(self):
        self.lcd.clear()

    def cleanup(self):
        self.clear()
        for pin in [self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7]:
            pin.deinit()
