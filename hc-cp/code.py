import usb_hid
import time
import digitalio
import board

from hid_joystick import Joystick
from analogio import AnalogIn

joy = Joystick(usb_hid.devices)

b0 = digitalio.DigitalInOut(board.GP0)
b0.direction = digitalio.Direction.INPUT
b0.pull = digitalio.Pull.UP
last_b0 = True
press_count = 0
axis_pos = 0

gp15 = digitalio.DigitalInOut(board.GP15)
gp15.direction = digitalio.Direction.OUTPUT
gp15.value = 1

analog_in = AnalogIn(board.A0)

# Equivalent of Arduino's map() function.
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    val = b0.value
    if last_b0 != val:
        last_b0 = val
        if val:
            print("Released", press_count)
            joy.release_buttons(1)
            gp15.value = 1
        else:
            press_count += 1
            print("Pressed", press_count)
            joy.press_buttons(1)
            gp15.value = 0
    in_raw = analog_in.value
    axis_pos = range_map(in_raw, 0, 65535, 0, 4095)
    #print("Remapped from to", in_raw, axis_pos)
    joy.move_joysticks(axis_pos, axis_pos, axis_pos, axis_pos)
    axis_pos += 1
    if axis_pos > 4095:
        axis_pos = 0
    time.sleep(0.2)
    #print("Analog", analog_in.value)

