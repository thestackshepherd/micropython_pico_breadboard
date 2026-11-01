"""_summary_
micropython pico python development file
"""

import time

from machine import Pin

from buzzer import Buzzer
from led import LED
from log import Log

BUZZER_PIN = 13
BUZZER_FREQUENCY = 1000

BLINK_INTERVAL_MS = 500
BEEP_INTERVAL_MS = 10000
LOOP_DELAY_MS = 10


def is_interval_elapsed(last_ms: int, now_ms: int, interval_ms: int) -> bool:
    """
    returns True once interval_ms has passed since last_ms.
    ticks_diff handles the ticks_ms counter wrapping around.
    """
    return time.ticks_diff(now_ms, last_ms) >= interval_ms


def main() -> None:
    """_summary_
    entry point of the application.
    """
    logger = Log()

    # setup: create the devices. nothing below can run without them.
    try:
        device_pico_led = LED(Pin("LED", Pin.OUT))
        gp13_device_buzzer = Buzzer(BUZZER_FREQUENCY, Pin(BUZZER_PIN))
        gp12_device_led = LED(Pin(12, Pin.OUT))
    except (ValueError, OSError) as e:
        # ValueError: bad pin id/name, OSError: hardware or driver failure
        logger.error(f"pico2w setup failed: {e}")
        return

    logger.info("setup complete, entering main loop")

    # super loop: check what is due, act on it, repeat.
    last_blink = last_beep = time.ticks_ms()
    try:
        while True:
            now: int = time.ticks_ms()

            if is_interval_elapsed(last_blink, now, BLINK_INTERVAL_MS):
                device_pico_led.toggle()
                last_blink = now

            #if is_interval_elapsed(last_beep, now, BEEP_INTERVAL_MS):
                #gp13_device_buzzer.play_sound()  # blocks for ~0.3s
                #last_beep = time.ticks_ms()

            if is_interval_elapsed(last_blink, now, BEEP_INTERVAL_MS):
                gp12_device_led.toggle()
                last_blink = now


            time.sleep_ms(LOOP_DELAY_MS)
    finally:
        # runs on Ctrl+C / Stop, so the led isn't left in a random state
        device_pico_led.turn_led_off()
        logger.info("main loop stopped")


if __name__ == "__main__":
    main()
