import os
import time

from macros.fight_actions import basic_attack_combo, basic_attack_combo_dodge
from macros.basic_actions import swipe_macro, tap_macro

from utils.screenshot_utils import check_template, find_coordinates, find_all_coordinates, match_in_roi, take_screenshot
from utils.paths import SCREENSHOT_DIR_FINAL, TEMPLATE_DIR

def check_close(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/close_button.png"

    for i in range(5):
        if check_template(adb_address, template_path, threshold=0.8):
            return True
        time.sleep(10)

def fight_until_close(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/close_button.png"

    for i in range(5):
        if check_template(adb_address, template_path, threshold=0.8):
            return True
        basic_attack_combo(adb_address)
        time.sleep(2)

def check_fight_skip(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/skip_button.png"

    for i in range(5):
        if check_template(adb_address, template_path, threshold=0.8):
            return True
        basic_attack_combo_dodge(adb_address)
        basic_attack_combo_dodge(adb_address)
        tap_macro(944, 493)  # Special Attack
        time.sleep(1)

def check_counter(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/counter.png"

    for i in range(5):
        if check_template(adb_address, template_path, threshold=0.8):
            return True
        basic_attack_combo_dodge(adb_address)
        basic_attack_combo_dodge(adb_address)
        tap_macro(944, 493)  # Special Attack
        time.sleep(1)

def draw_10x_till_1x(adb_address, *args):
    template_path_skip = f"{TEMPLATE_DIR}/skip_button.png"
    template_path_require = f"{TEMPLATE_DIR}/token_require.png"
    template_path_close = f"{TEMPLATE_DIR}/close_button.png"


    tap_macro(1146, 658) # Gacha 10x pull
    time.sleep(3)

    for i in range(15):
        if check_template(adb_address, template_path_skip, threshold=0.8):
            tap_macro(1180, 52)  # Skip
            time.sleep(2)
            tap_macro(1180, 52)  # Skip
            time.sleep(2)
        else:
            tap_macro(640, 664)  # Tap to close
            time.sleep(3)
            tap_macro(1146, 658)  # Gacha 10x pull
            time.sleep(3)

            if check_template(adb_address, template_path_close, threshold=0.8):
                if check_template(adb_address, template_path_require, threshold=0.8):
                    tap_macro(978, 203)  # Close token require
                    time.sleep(3)
                    return True
                
                tap_macro(868, 512)  # Confirm
                time.sleep(3)

def draw_1x_till_0(adb_address, *args):
    template_path_skip = f"{TEMPLATE_DIR}/skip_button.png"
    template_path_require = f"{TEMPLATE_DIR}/token_require.png"
    template_path_close = f"{TEMPLATE_DIR}/close_button.png"

    tap_macro(845, 657) # Gacha 1x pull
    time.sleep(3)

    for i in range(15):
        if check_template(adb_address, template_path_skip, threshold=0.8):
            tap_macro(1180, 52)  # Skip
            time.sleep(2)
            tap_macro(1180, 52)  # Skip
            time.sleep(2)
        else:
            tap_macro(640, 664)  # Tap to close
            time.sleep(3)
            tap_macro(845, 657)  # Gacha 1x pull
            time.sleep(3)

            if check_template(adb_address, template_path_close, threshold=0.8):
                if check_template(adb_address, template_path_require, threshold=0.8):
                    tap_macro(978, 203)  # Close token require
                    time.sleep(3)
                    return True
                
                tap_macro(868, 512)  # Confirm
                time.sleep(3)

def find_more(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/more.png"

    coords = find_coordinates(adb_address, template_path, threshold=0.8)
    
    if coords:
        tap_macro(coords[0], coords[1])
        time.sleep(1)
        return True

def final_screenshot(instance_name, *args):
    DIR = SCREENSHOT_DIR_FINAL
    ts = time.strftime("%H%M%S")
    FILENAME = f"Day1_{instance_name}_{ts}.png"
    take_screenshot(instance_name, DIR, FILENAME)