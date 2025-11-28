"""Game-specific actions"""

import os
import time

from macros.basic_actions import input_macro, tap_macro
from utils.screenshot_utils import check_template, find_coordinates
from utils.paths import MAIN_PATH, LUCK_NAME, PACKAGE_NAME, TEMPLATE_DIR

def launch_game(adb_address, *args):
    """Launch the game application
    
    Args:
        adb_address: ADB address of the device
    """
    os.system(f'adb -s {adb_address} shell monkey -p {PACKAGE_NAME} -c android.intent.category.LAUNCHER 1')
    
def clear_game(adb_address, *args):
    """Clear the game application data
    
    Args:
        adb_address: ADB address of the device
    """
    os.system(f'adb -s {adb_address} shell pm clear {PACKAGE_NAME}')
    time.sleep(5)

def quit_game(adb_address, *args):
    """Force close the game application
    
    Args:
        adb_address: ADB address of the device
    """
    os.system(f'adb -s {adb_address} shell am force-stop {PACKAGE_NAME}')

def quit_luck(adb_address, *args):
    """Force close the luck application
    
    Args:
        adb_address: ADB address of the device
    """
    os.system(f'adb -s {adb_address} shell am force-stop {LUCK_NAME}')

def open_luck(adb_address, luck_key, *args):
    """Launch the luck application
    
    Args:
        adb_address: ADB address of the device
    """
    os.system(f'adb -s {adb_address} shell monkey -p {LUCK_NAME} -c android.intent.category.LAUNCHER 1')
    time.sleep(18)

    tap_macro(adb_address, 500, 270)
    time.sleep(5)

    for i in range(16):
        os.system(f'adb -s {adb_address} shell input keyevent DEL')
    input_macro(adb_address, luck_key)
    time.sleep(6)

    tap_macro(adb_address, 230, 350)      # Done
    time.sleep(3)

    tap_macro(adb_address, 582, 821)
    time.sleep(4)

    tap_macro(adb_address, 545, 733)
    time.sleep(14)

    tap_macro(adb_address, 32, 254)
    time.sleep(3)

    tap_macro(adb_address, 32, 356)
    time.sleep(3)

    tap_macro(adb_address, 364, 886)
    time.sleep(6)

    tap_macro(adb_address, 545, 733)
    time.sleep(10)

    template_path = f"{TEMPLATE_DIR}/luck_checker.png"
    for i in range(3):
        if check_template(adb_address, template_path, threshold=0.8):
            tap_macro(adb_address, 545, 733)
            time.sleep(10)
            break
        else:
            time.sleep(5)

    os.system(f'adb -s {adb_address} shell monkey -p {PACKAGE_NAME} -c android.intent.category.LAUNCHER 1')
    time.sleep(20)

def open_game(adb_address, *args):
    """Launch the game application
    
    Args:
        adb_address: ADB address of the device
    """
    os.system(f'adb -s {adb_address} shell monkey -p {PACKAGE_NAME} -c android.intent.category.LAUNCHER 1')

def uninstall_game(adb_address, *args):
    """Uninstall the game application
    
    Args:
        adb_address: ADB address of the device
    """
    os.system(f'adb -s {adb_address} uninstall {PACKAGE_NAME}')