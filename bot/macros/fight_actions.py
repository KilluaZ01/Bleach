import os
import time

from macros.basic_actions import swipe_macro, tap_macro

def basic_attack_combo(adb_address, *args):
    """Perform a basic attack combo sequence
    
    Args:
        adb_address: ADB address of the device
        args: Additional arguments (not used)
    """
    for i in range(10):
        tap_macro(adb_address, 1068, 538)
        time.sleep(0.5)
    swipe_macro(adb_address, 1068, 533, 1068, 533, 2500)

def basic_attack_combo_dodge(adb_address, *args):
    """Perform a basic attack combo sequence
    
    Args:
        adb_address: ADB address of the device
        args: Additional arguments (not used)
    """
    tap_macro(adb_address, 951, 642)  # Dodge action
    time.sleep(0.5)
    for i in range(10):
        tap_macro(adb_address, 1068, 538)
        time.sleep(0.5)
    tap_macro(adb_address, 951, 642)  # Dodge action
    time.sleep(0.5)
    for i in range(10):
        tap_macro(adb_address, 1068, 538)
        time.sleep(0.5)
    swipe_macro(adb_address, 1068, 533, 1068, 533, 2500)
    