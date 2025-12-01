import os
import time

from macros.fight_actions import basic_attack_combo, basic_attack_combo_dodge
from macros.basic_actions import swipe_macro, tap_macro

from utils.screenshot_utils import check_template, find_coordinates, find_all_coordinates, match_in_roi, take_screenshot
from utils.paths import SCREENSHOT_DIR_FINAL, TEMPLATE_DIR

def check_close(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/close_button.png"

    for i in range(5):
        if check_template(adb_address, template_path, threshold=0.9):
            return True
        time.sleep(10)

def fight_until_close(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/close_button.png"

    for i in range(5):
        if check_template(adb_address, template_path, threshold=0.9):
            return True
        basic_attack_combo(adb_address)
        time.sleep(2)

def check_fight_skip(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/skip_button.png"
    template_path2 = f"{TEMPLATE_DIR}/skip_gatcha.png"

    for i in range(5):
        if check_template(adb_address, template_path, threshold=0.7) or check_template(adb_address, template_path2, threshold=0.7):
            tap_macro(adb_address, 1180, 52)
            time.sleep(2)
            tap_macro(adb_address, 870, 533)
            time.sleep(3)
            return True
        basic_attack_combo_dodge(adb_address)
        basic_attack_combo_dodge(adb_address)
        tap_macro(adb_address, 944, 493)  # Special Attack
        time.sleep(1)

def check_counter(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/counter.png"

    for i in range(5):
        if not check_template(adb_address, template_path, threshold=0.9):
            return True
        basic_attack_combo_dodge(adb_address)
        basic_attack_combo_dodge(adb_address)
        tap_macro(adb_address, 944, 493)  # Special Attack
        time.sleep(1)

def draw_10x_till_1x(adb_address, *args):
    template_path_skip = f"{TEMPLATE_DIR}/skip_gatcha.png"
    template_path_require = f"{TEMPLATE_DIR}/token_require.png"
    template_path_close = f"{TEMPLATE_DIR}/close_button.png"
    template_path_rate = f"{TEMPLATE_DIR}/rating.png"
    template_path_topup = f"{TEMPLATE_DIR}/top_up.png"

    tap_macro(adb_address, 1146, 658) # Gacha 10x pull
    time.sleep(3)

    for i in range(20):
        if check_template(adb_address, template_path_skip, threshold=0.9):
            tap_macro(adb_address, 1180, 52)  # Skip
            print('Skipping...')
            time.sleep(2)
            tap_macro(adb_address, 1180, 52)  # Skip
            print('Skipping...')
            time.sleep(2)
            
        else:
            print('Closing')
            tap_macro(adb_address, 640, 664)  # Tap to close
            time.sleep(3)
            
            print('Another 10')
            tap_macro(adb_address,  1146, 658)  # Gacha 10x pull
            time.sleep(3)
            

            if check_template(adb_address, template_path_close, threshold=0.9):
                if check_template(adb_address, template_path_require, threshold=0.9):
                    print('Close Token')
                    tap_macro(adb_address, 978, 203)  # Close token require
                    time.sleep(3)
                    return True
                
                elif check_template(adb_address, template_path_rate, threshold=0.8):
                    print('Close Token')
                    tap_macro(adb_address, 861, 64)  # Close token require
                    time.sleep(2)
                    
                print('Confirm')
                tap_macro(adb_address, 868, 512)  # Confirm
                time.sleep(3)
                
                if check_template(adb_address, template_path_topup, threshold=0.9):
                    tap_macro(adb_address, 54, 35)  # Return
                    time.sleep(2)
                    return True

def draw_till_next(adb_address, *args):
    template_path_skip = f"{TEMPLATE_DIR}/skip_gatcha.png"
    template_path_close = f"{TEMPLATE_DIR}/close_button.png"
    template_path_rate = f"{TEMPLATE_DIR}/rating.png"

    for i in range(20):
        if check_template(adb_address, template_path_skip, threshold=0.9):
            tap_macro(adb_address, 1180, 52)  # Skip
            time.sleep(2)
            tap_macro(adb_address, 1180, 52)  # Skip
            time.sleep(2)
        else:
            tap_macro(adb_address, 640, 664)  # Tap to close
            time.sleep(3)
            tap_macro(adb_address,  1146, 658)  # Gacha 10x pull
            time.sleep(3)

            if check_template(adb_address, template_path_close, threshold=0.9):
                tap_macro(adb_address, 978, 203)  # Close token require
                time.sleep(3)
                return True
            
            elif check_template(adb_address, template_path_rate, threshold=0.8):
                print('Close Token')
                tap_macro(adb_address, 861, 64)  # Close token require
                time.sleep(2)

def draw_1x_till_0(adb_address, *args):
    template_path_skip = f"{TEMPLATE_DIR}/skip_gatcha.png"
    template_path_topup = f"{TEMPLATE_DIR}/top_up.png"
    template_path_close = f"{TEMPLATE_DIR}/close_button.png"

    tap_macro(adb_address, 845, 657) # Gacha 1x pull
    time.sleep(3)

    for i in range(20):
        if check_template(adb_address, template_path_skip, threshold=0.9):
            tap_macro(adb_address, 1180, 52)  # Skip
            time.sleep(2)
            tap_macro(adb_address, 1180, 52)  # Skip
            time.sleep(2)
        else:
            tap_macro(adb_address, 640, 664)  # Tap to close
            time.sleep(3)
            tap_macro(adb_address, 845, 657)  # Gacha 1x pull
            time.sleep(3)

            if check_template(adb_address, template_path_close, threshold=0.9):
                tap_macro(adb_address, 868, 512)  # Confirm
                time.sleep(3)

                if check_template(adb_address, template_path_topup, threshold=0.9):
                    return True

def find_more(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/more.png"

    coords = find_coordinates(adb_address, template_path, threshold=0.9)
    
    if coords:
        x, y = coords
        tap_macro(adb_address, x, y)
        time.sleep(2)
        return True
    else:
        tap_macro(adb_address, 42, 661)
        time.sleep(2)

def final_screenshot(adb_address, *args):
    DIR = SCREENSHOT_DIR_FINAL
    ts = int(time.time())
    FILENAME = f"Day1_{adb_address}_{ts}.png"
    take_screenshot(adb_address, DIR, FILENAME)

def check_counter_text(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/counter_text.png"

    for i in range(3):
        if check_template(adb_address, template_path, threshold=0.9):
            return True
        time.sleep(5)

def check_track(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/track_text2.png"

    for i in range(5):
        if check_template(adb_address, template_path, threshold=0.9):
            return True
        basic_attack_combo(adb_address)
        time.sleep(1)
        tap_macro(adb_address, 946, 632)  # Dodge
        time.sleep(1)
        tap_macro(adb_address, 944, 493)  # Special Attack  
        time.sleep(10)

def check_timer(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/match3.png"

    if check_template(adb_address, template_path, threshold=0.9):
        basic_attack_combo(adb_address)
        time.sleep(1)
        basic_attack_combo(adb_address)
        time.sleep(1)
        swipe_macro(adb_address, 239, 533, 229, 347, 11000)
    else:
        return True

def sense_three(adb_address, *args):
    template_path = f"{TEMPLATE_DIR}/skip_button.png"
    for i in range(5):
        swipe_macro(adb_address, 645, 290, 645, 320, 1800)
        time.sleep(3)

        tap_macro(adb_address, 600, 1)
        time.sleep(4)
        
        if check_template(adb_address, template_path, threshold=0.7):
            return True
        
