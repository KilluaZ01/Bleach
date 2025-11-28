"""Basic tap and swipe actions"""

import os

def tap_macro(adb_address, x, y):
    """Perform a tap action on the specified instance
    
    Args:
        adb_address: ADB address of the device
        x: X coordinate
        y: Y coordinate
    """
    tap_command = f"adb -s {adb_address} shell input tap {x} {y}"
    os.system(tap_command)


def swipe_macro(adb_address, x1, y1, x2, y2, duration = 1000):
    """Perform a swipe action on the specified instance
    
    Args:
        adb_address: ADB address of the device
        x1, y1: Starting coordinates
        x2, y2: Ending coordinates
        duration: Duration of the swipe in milliseconds
    """
    swipe_command = f"adb -s {adb_address} shell input touchscreen swipe {x1} {y1} {x2} {y2} {duration}"
    os.system(swipe_command)

def input_macro(adb_address, name):
    """Input text into the specified instance
    
    Args:
        adb_address: ADB address of the device
        name: Text to input
    """
    input_command = f'adb -s {adb_address} shell input text "{name}"'
    os.system(input_command)

