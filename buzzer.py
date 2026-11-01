
"""__summary__
File represents the buzzer and buzzer operations on the kit.
"""
import time

from machine import PWM, Pin


class Buzzer:
    """_summary_
    Class represents the buzzer on the breadboard.
    """
    def __init__(self, frequency: int, buzzer_pin: Pin) -> None:
        self.buzzer: PWM = PWM(buzzer_pin)         # Define the Buzzer object
        self.buzzer_frequency: int = frequency     # Buzzer Freq Var.

    def _set_buzzer_frequency(self, frequency: int) -> None:
        self.buzzer.freq(frequency)

    def play_sound(self) -> None:
        """__summary__
        plays a sound with the buzzer on the breadboard
        """
        self.buzzer.init()
        self._set_buzzer_frequency(self.buzzer_frequency)
        self.buzzer.duty_u16(32768)   # 50% duty = sound on
        time.sleep(0.3)
        self.buzzer.duty_u16(0)       # off
        self.buzzer.deinit()
