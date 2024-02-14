import usb_hid
import supervisor

supervisor.set_usb_identification("me2d", "heli-controls")

HELI_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,                    # USAGE_PAGE (Generic Desktop)
    0x09, 0x04,                    # USAGE (Joystick)
    0xa1, 0x01,                    # COLLECTION (Application)
    0x85, 0x04,                    #   REPORT_ID (4)
    0x05, 0x09,                    #   USAGE_PAGE (Button)
    0x19, 0x01,                    #   USAGE_MINIMUM (Button 1)
    0x29, 0x20,                    #   USAGE_MAXIMUM (Button 32)
    0x15, 0x00,                    #   LOGICAL_MINIMUM (0)
    0x25, 0x01,                    #   LOGICAL_MAXIMUM (1)
    0x75, 0x01,                    #   REPORT_SIZE (1)
    0x95, 0x20,                    #   REPORT_COUNT (32)
    0x81, 0x02,                    #   INPUT (Data,Var,Abs)
    0x05, 0x01,                    #   USAGE_PAGE (Generic Desktop)
    0x09, 0x30,                    #   USAGE (X)
    0x15, 0x00,                    #   LOGICAL_MINIMUM (0)
    0x26, 0xff, 0x0f,              #   LOGICAL_MAXIMUM (4095)
    0x75, 0x0c,                    #   REPORT_SIZE (12)
    0x95, 0x01,                    #   REPORT_COUNT (1)
    0x81, 0x02,                    #   INPUT (Data,Var,Abs)
    0x75, 0x04,                    #   REPORT_SIZE (4)
    0x95, 0x01,                    #   REPORT_COUNT (1)
    0x81, 0x03,                    #   INPUT (Cnst,Var,Abs)
    0x05, 0x01,                    #   USAGE_PAGE (Generic Desktop)
    0x09, 0x31,                    #   USAGE (Y)
    0x15, 0x00,                    #   LOGICAL_MINIMUM (0)
    0x26, 0xff, 0x0f,              #   LOGICAL_MAXIMUM (4095)
    0x75, 0x0c,                    #   REPORT_SIZE (12)
    0x95, 0x01,                    #   REPORT_COUNT (1)
    0x81, 0x02,                    #   INPUT (Data,Var,Abs)
    0x75, 0x04,                    #   REPORT_SIZE (4)
    0x95, 0x01,                    #   REPORT_COUNT (1)
    0x81, 0x03,                    #   INPUT (Cnst,Var,Abs)
    0x05, 0x01,                    #   USAGE_PAGE (Generic Desktop)
    0x09, 0x32,                    #   USAGE (Z)
    0x15, 0x00,                    #   LOGICAL_MINIMUM (0)
    0x26, 0xff, 0x0f,              #   LOGICAL_MAXIMUM (4095)
    0x75, 0x0c,                    #   REPORT_SIZE (12)
    0x95, 0x01,                    #   REPORT_COUNT (1)
    0x81, 0x02,                    #   INPUT (Data,Var,Abs)
    0x75, 0x04,                    #   REPORT_SIZE (4)
    0x95, 0x01,                    #   REPORT_COUNT (1)
    0x81, 0x03,                    #   INPUT (Cnst,Var,Abs)
    0x05, 0x01,                    #   USAGE_PAGE (Generic Desktop)
    0x09, 0x33,                    #   USAGE (Rx)
    0x15, 0x00,                    #   LOGICAL_MINIMUM (0)
    0x26, 0xff, 0x0f,              #   LOGICAL_MAXIMUM (4095)
    0x75, 0x0c,                    #   REPORT_SIZE (12)
    0x95, 0x01,                    #   REPORT_COUNT (1)
    0x81, 0x02,                    #   INPUT (Data,Var,Abs)
    0x75, 0x04,                    #   REPORT_SIZE (4)
    0x95, 0x01,                    #   REPORT_COUNT (1)
    0x81, 0x03,                    #   INPUT (Cnst,Var,Abs)
    0xc0                           # END_COLLECTION
))

heli = usb_hid.Device(
    report_descriptor=HELI_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x04,                # Joystick
    report_ids=(4,),           # Descriptor uses report ID 4.
    in_report_lengths=(12,),    # This joy sends 12 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     usb_hid.Device.CONSUMER_CONTROL,
     heli)
)

