import board
import digitalio

adr_pins = [
  digitalio.DigitalInOut(board.GP6),
  digitalio.DigitalInOut(board.GP7),
  digitalio.DigitalInOut(board.GP8),
  digitalio.DigitalInOut(board.GP9)
]

for pin in adr_pins:
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = False

def set_channel(channel_num):
    adr_pins[0].value = channel_num & 1 > 0
    adr_pins[1].value = channel_num & 2 > 0
    adr_pins[2].value = channel_num & 4 > 0
    adr_pins[3].value = channel_num & 8 > 0
