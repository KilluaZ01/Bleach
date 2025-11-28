"""Game progression steps and execution"""

import time
import threading

from utils.screenshot_utils import take_screenshot

from macros import *

from .opencv_logics import *


def get_game_steps():
    """Get the complete list of game progression steps
    
    Returns:
        list: List of (description, function, coords, sleep_duration) tuples
    """

    steps = [
        ('Accept 1', tap_macro, (286, 329), 2),
        ('Accept 2', tap_macro, (286, 386), 2),
        ('Accept Confirm', tap_macro, (642, 487), 4),
        ('Notification', tap_macro, (640, 530), 370),
        ('Download Complete Checker', check_close, None, 2),
        ('Close', tap_macro, (1164, 87), 5),
        ('Guest Account', tap_macro, (764, 620), 10),
        ('Start', tap_macro, (645, 653), 34),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 26),
        ('Move Straight', swipe_macro, (239, 533, 229, 347, 2500), 3),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 1),
        ('Basic Attack', tap_macro, (1068, 538), 2),
        ('Move Straight', swipe_macro, (239, 533, 229, 347, 3000), 3),
        ('Special Attk', tap_macro, (944, 493), 12),
        ('Move Straight', swipe_macro, (239, 533, 229, 347, 6000), 7),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 18),
        ('Counter', tap_macro, (1177, 420), 3),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),  
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 4),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),  
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 4),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 17),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 4),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 4),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 4),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 4),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 4),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 4),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 4),
        ('Basic Attk', basic_attack_combo, (1068, 538), 40),
        ('Close In', tap_macro, (928, 684), 2),
        ('Close In', tap_macro, (928, 684), 18),
        ('Tap to Track', tap_macro, (120, 300), 9),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 6),
        ('Battle', tap_macro, (1205, 642), 6),
        ('Battle Mid', tap_macro, (660, 460), 4),
        ('Fight', tap_macro, (1052, 673), 4),
        ('Fight Start', tap_macro, (1130, 670), 25),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 10),
        ('Move Straight', swipe_macro, (239, 533, 229, 347, 3000), 4),
        ('Global', tap_macro, (600, 1), 3),
        ('Global', tap_macro, (600, 1), 6),
        ('Ultimate Attk', tap_macro, (1045, 406), 13),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Move Straight', swipe_macro, (239, 533, 229, 347, 11000), 15),
        ('Counter', tap_macro, (1177, 420), 3),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Basic Attk', tap_macro, (1068, 538), 1),
        ('Ultimate', tap_macro, (1045, 406), 9),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo', basic_attack_combo, None, 1),
        ('Basic Combo', basic_attack_combo, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo', basic_attack_combo, None, 1),
        ('Dodge', tap_macro, (946, 632), 1),
        ('Basic Combo', basic_attack_combo, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo', basic_attack_combo, None, 1),
        ('Basic Combo', basic_attack_combo, None, 1),
        ('Fight Until Close', fight_until_close, None, 1),
        ('Close Tut', tap_macro, (1117, 182), 3),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Ultimate Attk', tap_macro, (1045, 406), 12),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493) , 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Basic Attk', basic_attack_combo, (1068, 538), 1),
        ('Special Attk', tap_macro, (944, 493) , 3),
        ('Battle', tap_macro, (1205, 642), 6),
        ('Battle Mid', tap_macro, (660, 460), 4),
        ('Fight', tap_macro, (1052, 673), 4),
        ('Fight Start', tap_macro, (1130, 670), 26),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 4),
        ('Close Tut', tap_macro, (1118, 183), 2),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Ultimate Attk', tap_macro, (1045, 406), 3),
        ('Ultimate Attk', tap_macro, (1045, 406), 3),
        ('Ultimate Attk', tap_macro, (1045, 406), 7),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Check Skip Fight', check_fight_skip, None, 1),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 10),
        ('Close In', tap_macro, (928, 684), 2),
        ('Close In', tap_macro, (928, 684), 8),
        ('Tap to Close', tap_macro, (640, 664), 4),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 4),
        ('Character', tap_macro, (1092, 645), 6), 
        ('2nd Character', tap_macro, (42, 243), 3),
        ('Upgrade', tap_macro, (1013, 545), 3),
        ('Confirm Upgrade', tap_macro, (853, 574), 5),
        ('Tap to Close', tap_macro, (640, 664), 5),
        ('Return Main', tap_macro, (173, 37), 4),
        ('Battle', tap_macro, (1205, 642), 6),
        ('Battle Mid', tap_macro, (660, 460), 4),
        ('Fight', tap_macro, (1052, 673), 4),
        ('Add Char', tap_macro, (640, 397), 3),
        ('Select Char', tap_macro, (867, 161), 3),
        ('Deploy', tap_macro, (1053, 661), 4),
        ('Fight Start', tap_macro, (1130, 670), 26),
        ('Close Tut', tap_macro, (1118, 183), 2),
        ('Ultimate Attk', tap_macro, (1045, 406), 12),
        ('Special Attk', tap_macro, (944, 493), 4),
        ('Switch Char', tap_macro, (1190, 133), 3),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Ultimate Attk', tap_macro, (1045, 406), 7),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Basic Combo Dodge', basic_attack_combo_dodge, None, 1),
        ('Special Attk', tap_macro, (944, 493), 3),
        ('Check Counter', check_counter, None, 1),
        ('Close In', tap_macro, (928, 684), 2),
        ('Return to Main', tap_macro, (173, 37), 5),
        ('Tap to Track', tap_macro, (120, 300), 12),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 6),
        ('Tap to Track', tap_macro, (120, 300), 15),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 6),
        ('Talk to NPC', tap_macro, (798, 363), 3),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Talk Again', tap_macro, (977, 431), 6),
        ('First Sense', swipe_macro, (645, 290, 645, 320, 2800), 4),
        ('Global', tap_macro, (600, 1), 3),
        ('Second Sense', swipe_macro, (645, 290, 645, 320, 2600), 4), 
        ('Global', tap_macro, (600, 1), 4),
        ('Third Sense', swipe_macro, (645, 290, 645, 320, 1600), 3),
        ('Global', tap_macro, (600, 1), 4),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Confirm', tap_macro, (870, 533), 6),
        ('Tap to Close', tap_macro, (643, 560), 4),
        ('Global', tap_macro, (600, 1), 3),
        ('Global', tap_macro, (600, 1), 5),
        ('Global', tap_macro, (600, 1), 4),
        ('Go', tap_macro, (916, 454), 5),
        ('Gacha', tap_macro, (889, 651), 6),
        ('1x Gacha', tap_macro, (845, 657), 4),
        ('Skip', tap_macro, (1180, 52), 3),
        ('Tap to Close', tap_macro, (645, 661), 8),
        ('Return', tap_macro, (54, 35), 6),
        ('Event 1', tap_macro, (170, 588), 6),
        ('Claim All', tap_macro, (133, 650), 4)
        ('Tap to Close', tap_macro, (645, 622), 5),
        ('Tap to Close', tap_macro, (645, 670), 4),
        ('Return', tap_macro, (54, 35), 4),
        ('14 Days', tap_macro, (196, 583), 4),
        ('Claim 14', tap_macro, (327, 661), 4),
        ('Tap to Close', tap_macro, (645, 541),3),

        # ('Redeem Code', tap_macro, (133, 486), 4),
        # ('Input Code', tap_macro, (1075, 331), 3),
        # # Code Here
        # ('Ok', tap_macro, (1185, 258), 4),

        ('Return', tap_macro, (54, 35), 4),
        ('Close Notice', tap_macro, (1196, 93), 2),
        ('Close 14', tap_macro, (1193, 77), 2),
        ('Gacha', tap_macro, (889, 651), 6),
        ('Draw 10x Till 1x', draw_10x_till_1x, None, 1),
        ('Draw 1x Till 0', draw_1x_till_0, None, 1),
        ('Return', tap_macro, (54, 35), 4),
        ('Character', tap_macro, (1092, 645), 6), 
        ('Find More', find_more, None, 2),
        ('Final Screenshot',)
    ]
    
    return steps

def execute_macro_steps(guest_data, steps, log_func, pause_event):
    """Execute macro steps for all accounts in parallel
    
    Args:
        guest_data: List of (instance_name, guest_name) tuples
        steps: List of macro steps to execute
        log_func: Logging function
        pause_event: Threading event for pause control
    """

    for log_text, action_func, coords, sleep_duration in steps:
        pause_event.wait()
        log_func(log_text)

        if action_func == "input_name":
            for instance_name, guest_name, luck_key in guest_data:
                pause_event.wait()
                input_macro(instance_name, guest_name)
                log_func(f"[{instance_name}] Input guest name: {guest_name}")
            continue
        
        elif action_func == "luck_open":
            threads = []

            for instance_name, guest_name, luck_key in guest_data:

                # Skip instances without a luck code
                if not luck_key:
                    log_func(f"[{instance_name}] ⏸ No luck code — skipping luck macro")
                    continue

                pause_event.wait()

                # Threaded luck open
                t = threading.Thread(target=open_luck, args=(instance_name, luck_key))
                t.start()
                threads.append(t)

                log_func(f"[{instance_name}] Started luck thread using key: {luck_key}")

            # Join ALL luck threads
            for t in threads:
                t.join()

            log_func(f"➡ Finished threaded luck_open step: {log_text}")
            continue

        # Normal or validation steps
        threads = []
        bad_instances = []

        for instance_name, guest_name, luck_key in list(guest_data):  # iterate over COPY
            pause_event.wait()

            # Case 1: template validation step
            # if action_func == validate_template:
            #     template_name, threshold = coords  # coords passed as tuple
            #     ok = validate_template(instance_name, template_name, threshold)

            #     if not ok:
            #         log_func(f"[{instance_name}] FAILED validation: removing instance...")
            #         # Another Cycle Logic
            #         time.sleep(4)
            #         bad_instances.append((instance_name, guest_name, luck_key))
            #     continue  # no threading needed for validation

            # Case 2: normal threaded step
            if coords is not None:
                t = threading.Thread(target=action_func, args=(instance_name, *coords))
            else:
                t = threading.Thread(target=action_func, args=(instance_name,))

            t.start()
            threads.append(t)

        # Join threads
        for t in threads:
            t.join()

        # Remove bad instances
        for bad in bad_instances:
            guest_data.remove(bad)
            log_func(f"[Removed] {bad[0]} removed from guest_data")

        # If no instances left → stop early
        if not guest_data:
            log_func("All instances failed. Stopping automation…")
            break

        # Sleep
        for _ in range(sleep_duration):
            pause_event.wait()
            time.sleep(1)
