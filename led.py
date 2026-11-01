from machine import Pin, Timer


class LED:
    """
    represents an LED
    """
    def __init__(self, input_pin: Pin) -> None:
        self.pico_led = Pin(input_pin) # pin Definition
        self.tim = Timer(-1) # define software timer

    def tick(self, timer: Timer) -> None:
        """
        callback functionality for tim.init
        """
        self.pico_led.toggle()

    def blink_builtin_pico_led_indefinite(self) -> None:
        """
        method blinks the builtin pico led indefinitely
        """
        self.tim.init(freq=2, mode=Timer.PERIODIC, callback=self.tick)

    def turn_led_on(self) -> None:
        """
        method turns the led on
        """
        self.pico_led.value(1)

    def turn_led_off(self) -> None:
        """
        method turns the led off
        """
        self.pico_led.value(0)

    def toggle(self) -> None:
        """
        method flips the led: on becomes off, off becomes on
        """
        self.pico_led.toggle()

    def is_on(self) -> bool:
        """
        method returns True if the led is currently on, False if it is off
        """
        return self.pico_led.value() == 1
