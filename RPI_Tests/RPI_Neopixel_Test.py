# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import math


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 3

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def GetCycleRed(tick, animationDuration, offset) -> float:
    temporary = 0
    ratio = tick / animationDuration
    ratio = ratio * 6.28

    temporary = math.sin(ratio + offset)
    temporary = math.pow(temporary, 4) * 255

    return temporary

def GetCycleBlue(tick, animationDuration, offset) -> float:
    temporary = 0
    ratio = tick / animationDuration
    ratio = ratio * 6.28

    temporary = math.sin(ratio + offset + 2.09)
    temporary = math.pow(temporary, 4) * 255

    return temporary

def GetCycleGreen(tick, animationDuration, offset) -> float:
    temporary = 0
    ratio = tick / animationDuration
    ratio = ratio * 6.28

    temporary = math.sin(ratio + offset - 2.09)
    temporary = math.pow(temporary, 4) * 255

    return temporary


while True:

    for tick in range(628):
        cycledRed = GetCycleRed(tick, 628.0, -0.5)
        cycledBlue = GetCycleBlue(tick, 628.0, -0.5)
        cycledGreen = GetCycleGreen(tick, 628.0, -0.5)

        cycledRed1 = GetCycleRed(tick, 628.0, 0)
        cycledBlue1 = GetCycleBlue(tick, 628.0, 0)
        cycledGreen1 = GetCycleGreen(tick, 628.0, 0)

        cycledRed2 = GetCycleRed(tick, 628.0, 0.5)
        cycledBlue2 = GetCycleBlue(tick, 628.0, 0.5)
        cycledGreen2 = GetCycleGreen(tick, 628.0, 0.5)

        pixels[0] = (int(cycledRed), int(cycledGreen), int(cycledBlue))
        pixels[1] = (int(cycledRed1), int(cycledGreen1), int(cycledBlue1))
        pixels[2] = (int(cycledRed2), int(cycledGreen2), int(cycledBlue2))

        pixels

        pixels.show()
        time.sleep(0.001)