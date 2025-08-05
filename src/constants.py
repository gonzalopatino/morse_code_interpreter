# src/constants.py

# Morse code timing rules (in seconds)

DOT_DURATION = 0.5           # 1 time unit
DASH_DURATION = 3 * DOT_DURATION
INTRA_CHAR_GAP = DOT_DURATION            # Between dots and dashes in a character
INTER_CHAR_GAP = 3 * DOT_DURATION        # Between characters
INTER_WORD_GAP = 7 * DOT_DURATION        # Between words
