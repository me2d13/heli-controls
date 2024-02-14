import usb_hid
import time
import digitalio
import board
import cyclic
import collective
import mux
import supervisor

from hid_joystick import Joystick
from analogio import AnalogIn

do_profiling = False
steps_batch = 100

joy = Joystick(usb_hid.devices, False)

step_no = 0
start_msecs = supervisor.ticks_ms()
while True:
    #time.sleep(0.2)
    #cyclic.describe()
    #collective.describe()
    for channel in range(16):
        mux.set_channel(channel)
        cyclic.buttons(joy, channel)
    cyclic.loop(joy)
    collective.loop(joy)
    joy._send()
    if do_profiling:
        step_no += 1
        if step_no > steps_batch:
            elapsed_ms = supervisor.ticks_ms() - start_msecs
            print("Average step in ms", elapsed_ms/steps_batch)
            step_no = 0
            start_msecs = supervisor.ticks_ms()
