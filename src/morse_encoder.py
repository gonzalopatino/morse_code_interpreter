# src/morse_encoder.py

class MorseEncoder:
    def __init__(self):
        self.morse_dict = {
            'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
            'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
            'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
            'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',
            'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
            'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
            'Y': '-.--',  'Z': '--..',
            '1': '.----', '2': '..---', '3': '...--', '4': '....-',
            '5': '.....', '6': '-....', '7': '--...', '8': '---..',
            '9': '----.', '0': '-----',
            ' ': '/'  # Special case: word separator
        }

    def encode(self, message: str) -> list[str]:
        return [self.morse_dict.get(char, '') for char in message.upper()]
