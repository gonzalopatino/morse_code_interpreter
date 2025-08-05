# Morse Code Interpreter Project
By Gonzalo Patino

## Description
This Python application runs a finite state machine (FSM) that converts predefined messages to Morse code using LEDs and a 16x2 LCD display. It supports button input to skip messages.

## Hardware Requirements
- Raspberry Pi 4
- 2 LEDs (Red and Blue)
- 16x2 Character LCD (HD44780 compatible)
- Push Button
- Breadboard and GPIO wiring

## Software Requirements
- Python 3.7+
- RPi.GPIO
- adafruit-circuitpython-charlcd

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
