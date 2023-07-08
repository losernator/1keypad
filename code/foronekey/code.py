# version:0.1
# author: losernator
# license: MIT

import time
import board
import digitalio
import usb_hid
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

key_pins = [board.GP0]
key_pins_array = []

keys_pressed = [[Keycode.C,Keycode.V]]
control_keys = [[Keycode.CONTROL,Keycode.CONTROL]]

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

for pin in key_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pins_array.append(key_pin)


# color preset
RED = (255,  0,  0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 40, 0)
CYAN = (0, 250, 250)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
GREY = (30, 30, 30)
WHITE = (250, 250, 250)
TEAL = (0, 255, 120)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)
BLACK = (0, 0, 0) # black or off
GOLD = (255, 222, 30)
PINK = (242, 90, 255)
AQUA = (50, 255, 255)
JADE = (0, 255, 40)
AMBER = (255, 100, 0)

num_pixels = len(key_pins)
pixels = neopixel.NeoPixel(board.GP29, num_pixels, auto_write=False)
pixels.brightness = 0.5
ledcolor = [PINK]
fadingstep = -10

def pixelfading(index):
    if pixels[index][0]+pixels[index][1]+pixels[index][2] > 0:
        modifier = fadingstep
        pixels[index]=(max([pixels[index][0]+ modifier,0]), max([pixels[index][1]+ modifier,0]), max([pixels[index][2]+ modifier,0]))

delay_time = 0.3

while True:
    for i, key_pin in enumerate(key_pins_array):
        if not key_pin.value:
            current = time.monotonic()
            pixels[i] = ledcolor[i]
            keys = keys_pressed[i]
            controls= control_keys[i]
            while not key_pin.value:
                pass
            if time.monotonic() - current < delay_time:
                print ("short!")
                if isinstance(keys[0],str):
                    keyboard_layout.write(keys[0])
                else:
                    keyboard.press(controls[0],keys[0])
                    keyboard.release_all()
            else:
                print ("long!")
                if isinstance(keys[1],str):
                    keyboard_layout.write(keys[1])
                else:
                    keyboard.press(controls[1],keys[1])
                    keyboard.release_all()
        else:
            pixelfading(i)
    pixels.show()
    time.sleep(0.01)

