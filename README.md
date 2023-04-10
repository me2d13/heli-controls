# heli-controls
Arduino software and notes for collective and cyclic build for flight simulation based on Karl Clarke's awesome models.

## Links
* [Build guides](https://www.737diysim.com/copy-3-of-build-guides-1)

## Design
I made a few changes in wiring. Instead of Leo Bodnar's board I used [arduino pro micro](https://learn.sparkfun.com/tutorials/pro-micro--fio-v3-hookup-guide/hardware-overview-pro-micro) and [I2C ADS1115 ADS1015 module](https://www.google.com/search?q=I2C+ADS1115+ADS1015) to increase precision. Pro micro doesn't have enough pins to read all buttons and controls servo motors so I used additonal [Arduino Uno](https://docs.arduino.cc/hardware/uno-rev3) with [CNC shield](https://www.google.com/search?q=arduino+cnc+shield+v3) to save some soldering. Also for all the buttons I have some [multiplexer](https://www.google.com/search?q=CD74HC4067+module) to keep number of wires low.

So Pro Micro is reading buttons, reading ADC converter and acting as joysting for the PC. Uno is controlling servo motors. Communication between Pro Micro and Uno is done via serial port with simple protocol.
