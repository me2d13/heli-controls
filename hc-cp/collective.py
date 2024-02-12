import board
import digitalio
from analogio import AnalogIn
from hid_joystick import Joystick
from tools import range_map

# joy assignments and calibration
joy_ftr_button = 2
joy_z_min = 0
joy_z_max = 65600
joy_z_zero = 24000


pin_buttons_1 = digitalio.DigitalInOut(board.GP3)
pin_buttons_1.direction = digitalio.Direction.INPUT
pin_buttons_1.pull = digitalio.Pull.UP

pin_buttons_2 = digitalio.DigitalInOut(board.GP4)
pin_buttons_2.direction = digitalio.Direction.INPUT
pin_buttons_2.pull = digitalio.Pull.UP

pin_ftr = digitalio.DigitalInOut(board.GP5)
pin_ftr.direction = digitalio.Direction.INPUT
pin_ftr.pull = digitalio.Pull.UP

pin_step = digitalio.DigitalInOut(board.GP1)
pin_dir = digitalio.DigitalInOut(board.GP0)
pin_en = digitalio.DigitalInOut(board.GP2)

pin_step.direction = digitalio.Direction.OUTPUT
pin_dir.direction = digitalio.Direction.OUTPUT
pin_en.direction = digitalio.Direction.OUTPUT

pin_step.value = False
pin_dir.value = False
pin_en.value = True

axis_z = AnalogIn(board.A2)

last_z = 32000
last_ftr = True

def describe():
    print("Collective state: Z", last_z,", ftr", pin_ftr.value)

def loop(joy: Joystick):
    global last_z, last_ftr
    cur_z = (65535 - axis_z.value + joy_z_zero) % 65535 # reversed
    cur_ftr = pin_ftr.value
    if last_z != cur_z:
        last_z = cur_z
        mapped_z = range_map(cur_z, joy_z_min, joy_z_max, 0, 4095)
        joy.move_joysticks(z=mapped_z)
    if cur_ftr != last_ftr:
        last_ftr = cur_ftr
        if cur_ftr:
            joy.release_buttons(joy_ftr_button)
            pin_en.value = False
        else:
            joy.press_buttons(joy_ftr_button)
            pin_en.value = True


