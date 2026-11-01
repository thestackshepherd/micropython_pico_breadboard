"""__summary__
File represents the RGB led on the breadboard. it is an addressable (WS2812 /
NeoPixel) led: one data pin, and the red, green and blue levels are sent to it
as data, instead of driving three pins.
"""
from collections import namedtuple

from machine import Pin
from neopixel import NeoPixel

MAX_CHANNEL = 255

# one row per color channel: the channel's name and its level (0-255).
Channel = namedtuple("Channel", ("name", "value"))


class RGBLED:
    """
    represents an addressable RGB led. brightness of each color channel is set
    from 0 (off) to 255 (full), and mixing the three makes other colors.
    """
    def __init__(self, data_pin: Pin) -> None:
        self.pixel = NeoPixel(data_pin, 1)  # a single led, so a strip of 1
        self.color = (
            Channel("red", 0),
            Channel("green", 0),
            Channel("blue", 0),
        )
        self.off()

    def set_color(self, red: int, green: int, blue: int) -> None:
        """
        method sets the color, each channel from 0 to 255
        """
        self.color = (
            Channel("red", max(0, min(MAX_CHANNEL, red))),
            Channel("green", max(0, min(MAX_CHANNEL, green))),
            Channel("blue", max(0, min(MAX_CHANNEL, blue))),
        )
        self.pixel[0] = (
            self.color[0].value, self.color[1].value, self.color[2].value
        )
        self.pixel.write()  # nothing changes on the led until write() is called

    def off(self) -> None:
        """
        method turns the led off
        """
        self.set_color(0, 0, 0)

    def is_on(self) -> bool:
        """
        method returns True if any channel is lit, False if all are off
        """
        return any(level.value > 0 for level in self.color)
