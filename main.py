"""_summary_
micropython pico python development file
"""

from machine import Pin

from buzzer import Buzzer
from led import LED
from log import Log


def main() -> None:
    """_summary_
    entry point of the application.
    """
    logger = Log()
    try:
        builtin_pico_led = LED(Pin("LED", Pin.OUT))
        if not builtin_pico_led.is_on():
            builtin_pico_led.turn_led_on()
        logger.info(f"pico2w led status: {builtin_pico_led.is_on()}")
        # builtin_pico_led.blink_builtin_pico_led_indefinite()
        # buzzer = Buzzer(1000, Pin(13))
        # buzzer.play_sound()
    except (ValueError, OSError) as e:
        # ValueError: bad pin id/name, OSError: hardware or driver failure
        logger.error(f"pico2w led setup failed: {e}")

if __name__ == "__main__":
    main()
