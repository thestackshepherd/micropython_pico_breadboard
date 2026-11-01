import time

from machine import SPI, Pin

# Pins from the EP-0172 wiki
SCK, MOSI, CS, DC, RST = 2, 3, 5, 6, 7
W, H = 320, 480


def color565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)


class ST7796:
    def __init__(self):
        self.spi = SPI(
            0,
            baudrate=40_000_000,
            polarity=0,
            phase=0,
            sck=Pin(SCK),
            mosi=Pin(MOSI)
        )
        self.cs = Pin(CS, Pin.OUT, value=1)
        self.dc = Pin(DC, Pin.OUT, value=0)
        self.rst = Pin(RST, Pin.OUT, value=1)
        self._init()

    # --- layer 1: raw bus. DC low = command, DC high = data ---
    def cmd(self, c, data=None):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([c]))
        if data:
            self.dc(1)
            self.spi.write(data)
        self.cs(1)

    # --- layer 2: controller setup ---
    def _init(self):
        self.rst(0); time.sleep_ms(50)
        self.rst(1); time.sleep_ms(120)
        self.cmd(0x01); time.sleep_ms(120)       # software reset
        self.cmd(0x11); time.sleep_ms(120)       # sleep out
        self.cmd(0xF0, b"\xC3")                  # unlock extended commands
        self.cmd(0xF0, b"\x96")
        self.cmd(0x36, b"\x48")                  # MADCTL: orientation / RGB order
        self.cmd(0x3A, b"\x55")                  # COLMOD: 16-bit RGB565
        self.cmd(0xF0, b"\x3C")                  # relock
        self.cmd(0xF0, b"\x69")
        self.cmd(0x21)
        self.cmd(0x29); time.sleep_ms(20)        # display on

    # --- layer 3: windowing. Every draw = set window, then stream pixels ---
    def window(self, x0, y0, x1, y1):
        self.cmd(0x2A, bytes([x0 >> 8, x0 & 255, x1 >> 8, x1 & 255]))
        self.cmd(0x2B, bytes([y0 >> 8, y0 & 255, y1 >> 8, y1 & 255]))
        self.cmd(0x2C)                           # RAMWR: pixel data follows

    # --- layer 4: drawing. One row of RAM, reused h times ---
    def fill_rect(self, x, y, w, h, color):
        self.window(x, y, x + w - 1, y + h - 1)
        row = bytes([color >> 8, color & 255]) * w
        self.cs(0)
        self.dc(1)
        for _ in range(h):
            self.spi.write(row)
        self.cs(1)

    def fill(self, color):
        self.fill_rect(0, 0, W, H, color)


def demo():
    d = ST7796()
    d.fill(color565(256, 256, 256))
    d.fill_rect(20, 20, 100, 60, color565(255, 0, 0))
    d.fill_rect(20, 100, 100, 60, color565(0, 255, 0))
    d.fill_rect(20, 180, 100, 60, color565(0, 0, 255))
    return d
