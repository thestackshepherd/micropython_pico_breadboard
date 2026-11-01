"""_summary_
micropython pico python development file
main method, contains super loop.
"""

import time

from machine import Pin

from buzzer import Buzzer
from led import LED
from log import Log
from rgb_led import RGBLED

BUZZER_PIN = 13
BUZZER_FREQUENCY = 1000

BLINK_INTERVAL_MS = 500
BEEP_INTERVAL_MS = 10000
BEEP_DURATION_MS = 300
LOOP_DELAY_MS = 10

# dim red: a WS2812 at full brightness (255) is very bright
RGB_LED_COLOR = (40, 0, 0)


def is_interval_elapsed(last_ms: int, now_ms: int, interval_ms: int) -> bool:
    """
    returns True once interval_ms has passed since last_ms.
    ticks_diff handles the ticks_ms counter wrapping around.
    """
    return time.ticks_diff(now_ms, last_ms) >= interval_ms

def killall(
        logger: Log,
        pico_device_led: LED,
        gp12_device_rgbled: RGBLED,
        gp13_device_buzzer: Buzzer,
    ) -> None:
    """
    turns off all devices, so the pico isn't left in a random state.
    uses the devices main() already created: building new ones would put a
    second NeoPixel, PWM and Timer on the same pins.
    """
    # Try to turn off pico led
    try:
        pico_device_led.turn_led_off()
        logger.info(f"pico_device_led status: {pico_device_led.is_on()}")
    except (ValueError, OSError) as e:
        logger.error(f"failed to turnoff pico led light: {e}")
    # Try to turn off gp12 rgb led
    try:
        gp12_device_rgbled.off()
        logger.info(f"gp12_device_rgbled status: {gp12_device_rgbled.is_on()}")
    except (ValueError, OSError) as e:
        logger.error(f"failed to turnoff gp12 rgb led light: {e}")
    # Try to turn off gp13 buzzer
    try:
        gp13_device_buzzer.stop_sound()
        logger.info(f"gp13_device_buzzer status: {gp13_device_buzzer.is_playing()}")
    except (ValueError, OSError) as e:
        logger.error(f"failed to turnoff gp13 buzzer: {e}")

def main() -> None:
    """_summary_
    entry point of the application.
    """
    logger = Log()

    # setup: create the devices. nothing below can run without them.
    try:
        pico_device_led    = LED(Pin("LED", Pin.OUT))
        gp13_device_buzzer = Buzzer(BUZZER_FREQUENCY, Pin(BUZZER_PIN))
        gp12_device_rgbled = RGBLED(Pin(12, Pin.OUT))
        gp12_device_rgbled.set_color(*RGB_LED_COLOR)  # lit right away, not after an interval
    except (ValueError, OSError) as e:
        # ValueError: bad pin id/name, OSError: hardware or driver failure
        logger.error(f"pico2w setup failed: {e}")
        return
    except Exception as e:  # noqa: BLE001  # pylint: disable=broad-exception-caught
        # anything else is a bug: log what it was instead of dying silently
        logger.error(f"unexpected {type(e).__name__} during setup: {e}")
        return

    logger.info("setup complete, entering main loop")

    # --- super loop: check what is due, act on it, repeat. ---------

    # Initialize the last action times to the current time,
    # first action will be delayed by the interval.
    last_pico_device_led_blink      = time.ticks_ms()
    last_gp13_device_buzzer_beep    = time.ticks_ms()
    try:
        while True:
            now: int = time.ticks_ms()

            if is_interval_elapsed(last_pico_device_led_blink, now, BLINK_INTERVAL_MS):
                pico_device_led.toggle()
                last_pico_device_led_blink = now

            if is_interval_elapsed(last_gp13_device_buzzer_beep, now, BEEP_INTERVAL_MS):
                gp13_device_buzzer.beep(BEEP_DURATION_MS)  # returns at once, a timer ends it
                last_gp13_device_buzzer_beep = now

            time.sleep_ms(LOOP_DELAY_MS)
    except KeyboardInterrupt:
        logger.info("main loop interrupted by user")
    except Exception as e:  # noqa: BLE001  # pylint: disable=broad-exception-caught
        # anything unexpected: log what it was, then fall through to killall()
        logger.error(f"unexpected {type(e).__name__} in main loop: {e}")
    finally:
        # runs on Ctrl+C / Stop, so the led isn't left in a random state
        killall(logger, pico_device_led, gp12_device_rgbled, gp13_device_buzzer)
        logger.info("main loop stopped")


if __name__ == "__main__":
    main()
