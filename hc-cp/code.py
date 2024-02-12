import usb_hid
import time
import digitalio
import board
import cyclic
import collective

from hid_joystick import Joystick
from analogio import AnalogIn

joy = Joystick(usb_hid.devices)

while True:
    #time.sleep(0.2)
    #cyclic.describe()
    #collective.describe()
    cyclic.loop(joy)
    collective.loop(joy)

