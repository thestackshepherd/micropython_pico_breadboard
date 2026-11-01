
"""__summary__
File represents the buzzer and buzzer operations on the kit.
"""

from machine import PWM, Pin, Timer

VOLUME_MAX = 65535
VOLUME_MIN = 0
class Buzzer:
    """_summary_
    Class represents the buzzer on the breadboard.
    """
    def __init__(self, frequency: int, buzzer_pin: Pin) -> None:
        self.buzzer: PWM = PWM(buzzer_pin)       # Define the Buzzer object
        self.buzzer.freq(frequency)              # Buzzer Freq Var.
        self.tim = Timer(-1)                     # one-shot timer that ends a beep
        self.slider = {
            "off":        VOLUME_MIN,
            # integer math (//): duty_u16 needs an int, a float raises TypeError
            "very-low":   VOLUME_MAX // 8,      # 1/8 of full volume
            "low":        VOLUME_MAX // 4,      # 1/4 of full volume
            "medium":     3 * VOLUME_MAX // 8,  # 3/8 of full volume
            "half":       VOLUME_MAX // 2,      # 1/2 of full volume
            "high":       5 * VOLUME_MAX // 8,  # 5/8 of full volume
            "extra-high": 6 * VOLUME_MAX // 8,  # 3/4 of full volume
            "extreme":    7 * VOLUME_MAX // 8,  # 7/8 of full volume
            "full":       VOLUME_MAX,           # full volume
        }

    def play_sound(self) -> None:
        """__summary__
        starts the sound and returns right away. it keeps sounding until
        stop_sound() is called, so the caller decides when to stop it.
        """
        self.buzzer.duty_u16(self.slider["very-low"])  # duty > 0 = sound on

    def beep(self, duration_ms: int) -> None:
        """_summary_
        sounds the buzzer for duration_ms, then silences it. returns right away:
        a one-shot timer does the stopping, so the caller never waits.
        """
        self.play_sound()
        self.tim.init(mode=Timer.ONE_SHOT, period=duration_ms, callback=self._end_beep)

    def _end_beep(self, _timer: Timer) -> None:
        """_summary_
        timer callback, runs in interrupt context: keep it short, no allocation.
        """
        self.buzzer.duty_u16(VOLUME_MIN)

    def stop_sound(self) -> None:
        """_summary_
        stops the buzzer from playing sound, and cancels a pending beep timer
        """
        self.tim.deinit()
        self.buzzer.duty_u16(self.slider["off"])  # 0% duty = sound off

    def is_playing(self) -> bool:
        """_summary_
        returns True if the buzzer is currently sounding, False if it is silent
        """
        return self.buzzer.duty_u16() > VOLUME_MIN
