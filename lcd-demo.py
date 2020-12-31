#!/usr/bin/python3

"""
    Program: LCD1602 Demo with HC-SR04 Sensor (lcd-demo.py)
    Author:  M. Heidenreich, (c) 2020

    Description:
    
    This code is provided in support of the following YouTube tutorial:
    https://youtu.be/DHbLBTRpTWM

    This example shows how to use the LCD1602 I2C display and the HC-SR04 sensor
    with Raspberry Pi using a multi-threaded approach.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE
    AUTHOR DISCLAIMS ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from signal import signal, SIGTERM, SIGHUP, pause
from time import sleep
from threading import Thread
from gpiozero import DistanceSensor
from rpi_lcd import LCD

reading = True
message = ""

lcd = LCD()
sensor = DistanceSensor(echo=20, trigger=21)

def safe_exit(signum, frame):
    exit(1)

def display_distance():
    while reading:
        lcd.text(message, 1)
        sleep(0.25)

def read_distance():
    global message

    while reading:
        message = f"Distance: {sensor.value:1.2f} m"
        print(message)

        sleep(0.1)

try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    reader = Thread(target=read_distance, daemon=True)
    display = Thread(target=display_distance, daemon=True)

    reader.start()
    display.start()

    pause()

except KeyboardInterrupt:
    pass

finally:
    reading = False
    sleep(0.5)
    lcd.clear()
    sensor.close()
