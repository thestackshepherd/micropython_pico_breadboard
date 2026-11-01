"""__summary__
File represents an RGB led: three leds (red, green, blue) in one package.
"""
from collections import namedtuple

from machine import PWM, Pin

PWM_FREQUENCY = 1000
MAX_CHANNEL = 255
MAX_DUTY = 65535

# one row per color channel: the channel's name and what it holds. the same shape
# is used for the pwm outputs (value is a PWM) and the color levels (value is 0-255).
Channel = namedtuple("Channel", ("name", "value"))


class RGBLED:
    """
    represents an RGB led. each color channel is driven with pwm, so its
    brightness can be set from 0 (off) to 255 (full), and mixing the three
    channels makes other colors.
    """
    def __init__(self,
            red_pin:      Pin,
            green_pin:    Pin,
            blue_pin:     Pin,
            common_anode: bool = False
        ) -> None:
        # common_anode: the shared pin goes to 3.3V, so a channel lights when its
        # pin is low. common cathode (the default): shared pin goes to GND.
        self.channels = (
            Channel("red", PWM(red_pin)),
            Channel("green", PWM(green_pin)),
            Channel("blue", PWM(blue_pin)),
        )
        self.common_anode: bool = common_anode
        self.color = (
            Channel("red", 0),
            Channel("green", 0),
            Channel("blue", 0),
        )

        for channel in self.channels:
            channel.value.freq(PWM_FREQUENCY)
        self.off()

    def set_color(self, red: int, green: int, blue: int) -> None:
        """
        method sets the color, each channel from 0 to 255
        """
        levels = (red, green, blue)
        self.color = tuple(
            Channel(output.name, max(0, min(MAX_CHANNEL, level)))
            for output, level in zip(self.channels, levels)
        )
        for output, level in zip(self.channels, self.color):
            duty = level.value * MAX_DUTY // MAX_CHANNEL
            if self.common_anode:
                duty = MAX_DUTY - duty
            output.value.duty_u16(duty)

    def off(self) -> None:
        """
        method turns all three channels off
        """
        self.set_color(0, 0, 0)

    def is_on(self) -> bool:
        """
        method returns True if any channel is lit, False if all are off
        """
        return any(level.value > 0 for level in self.color)
