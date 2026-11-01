# micropython-pico-breadboard

## What is this project

this project is a controller for the TFT Pico BreadBoard Kit Plus w/ Capacitive Touch
for Pico by 52Pi. [you can find information about the board here](https://wiki.52pi.com/index.php?title=EP-0172)

MicroPython code for a Raspberry Pi Pico 2 W on a breadboard. Edited and run with the
[MicroPico](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) VS Code extension.

`main.py` is the entry point the Pico runs on boot.

Additonally, for information about using MicroPython with the pico 2 [you can read
about that here.](https://pip-assets.raspberrypi.com/categories/610-raspberry-pi-pico/documents/RP-008355-DS-1-raspberry-pi-pico-python-sdk.pdf)

## Setup

Flash MicroPython for the Pico 2 W once: hold BOOTSEL, plug in, and drop the `.uf2` from
<https://micropython.org/download/RPI_PICO2_W/> onto the `RPI-RP2` drive.

## Usage

Open the folder in VS Code, connect the board, then use the MicroPico commands:

- **Run current file** to run `main.py` without saving it to the board
- **Upload project** to copy it to the board so it runs on every boot
