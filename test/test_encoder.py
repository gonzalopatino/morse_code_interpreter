# test/test_encoder.py

import sys
import os

# Add src directory to Python path so we can import morse_encoder
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from morse_encoder import MorseEncoder

def test_hello_world():
    encoder = MorseEncoder()
    message = "HELLO WORLD"
    expected = ['....', '.', '.-..', '.-..', '---', '/', '.--', '---', '.-.', '.-..', '-..']
    result = encoder.encode(message)

    print("Input   :", message)
    print("Expected:", expected)
    print("Result  :", result)

    assert result == expected, "Test failed: Morse encoding incorrect"
    print("✅ Test passed")

if __name__ == "__main__":
    test_hello_world()
