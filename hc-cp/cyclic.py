import board
import digitalio
from analogio import AnalogIn
from hid_joystick import Joystick
from tools import range_map

# joy assignments and calibration
joy_ftr_button = 1
joy_x_min = 7000
joy_x_max = 38000
joy_y_min = 15000
joy_y_max = 43000

joy_total_buttons = 8

#joy_x_max = 65535
#joy_y_max = 65535


pin_buttons = digitalio.DigitalInOut(board.GP10)
pin_buttons.direction = digitalio.Direction.INPUT
pin_buttons.pull = digitalio.Pull.UP

pin_ftr = digitalio.DigitalInOut(board.GP11)
pin_ftr.direction = digitalio.Direction.INPUT
pin_ftr.pull = digitalio.Pull.UP

axis_x = AnalogIn(board.A0)
axis_y = AnalogIn(board.A1)

pin_x_step = digitalio.DigitalInOut(board.GP20)
pin_x_dir = digitalio.DigitalInOut(board.GP19)
pin_x_en = digitalio.DigitalInOut(board.GP21)

pin_x_step.direction = digitalio.Direction.OUTPUT
pin_x_dir.direction = digitalio.Direction.OUTPUT
pin_x_en.direction = digitalio.Direction.OUTPUT

pin_x_step.value = False
pin_x_dir.value = False
pin_x_en.value = True

pin_y_step = digitalio.DigitalInOut(board.GP17)
pin_y_dir = digitalio.DigitalInOut(board.GP16)
pin_y_en = digitalio.DigitalInOut(board.GP18)

pin_y_step.direction = digitalio.Direction.OUTPUT
pin_y_dir.direction = digitalio.Direction.OUTPUT
pin_y_en.direction = digitalio.Direction.OUTPUT

pin_y_step.value = False
pin_y_dir.value = False
pin_y_en.value = True


last_x = 32000
last_y = 32000
last_ftr = True

last_buttons = [True for _ in range(0, joy_total_buttons)]

def describe():
    print("Cyclic state: X", axis_x.value,", Y", axis_y.value, ", ftr", pin_ftr.value)

def loop(joy: Joystick):
    global last_x, last_y, last_ftr
    cur_x = axis_x.value
    cur_y = axis_y.value
    cur_ftr = pin_ftr.value
    if last_x != cur_x or last_y != cur_y:
        last_x = cur_x
        last_y = cur_y
        mapped_x = range_map(cur_x, joy_x_min, joy_x_max, 0, 4095)
        mapped_y = range_map(cur_y, joy_y_min, joy_y_max, 0, 4095)
        joy.move_joysticks(x=mapped_x, y=mapped_y)
    if cur_ftr != last_ftr:
        last_ftr = cur_ftr
        if cur_ftr:
            joy.release_buttons(joy_ftr_button)
            pin_x_en.value = False
            pin_y_en.value = False
        else:
            joy.press_buttons(joy_ftr_button)
            pin_x_en.value = True
            pin_y_en.value = True

def buttons(joy: Joystick, button_channel):
    global last_buttons
    cur_button = pin_buttons.value
    if button_channel < joy_total_buttons and cur_button != last_buttons[button_channel]:
        last_buttons[button_channel] = cur_button
        joy_button_number = 3 + button_channel
        joy.release_buttons(joy_button_number) if cur_button else joy.press_buttons(joy_button_number)
