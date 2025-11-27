"""Account setup and validation"""

import os
from datetime import datetime

from utils.file_manager import save_account_metadata, backup_account_data
from utils.screenshot_utils import check_template
from utils.paths import SCREENSHOT_DIR_FINAL, TEMPLATE_DIR, SCREENSHOT_DIR

from macros.game_actions import quit_game

import time

def validate_accounts(guest_data, log_func):
    """Validate accounts and save successful ones
    
    Args:
        guest_data: List of (adb_address, guest_name, luck_code) tuples
        log_func: Logging function
        
    Returns:
        tuple: (valid_instances, valid_guest_names)
    """
    template_path = f"{TEMPLATE_DIR}/validate_end.png"
    final_dir = SCREENSHOT_DIR_FINAL
    valid_instances = []
    valid_guest_names = []

    for adb_address, guest_name, luck_code in guest_data:
        log_func(f"[{adb_address}] Taking screenshot for {guest_name}")

        if check_template(adb_address, template_path, final_dir, threshold=0.80):
            log_func(f"[{adb_address}] ✅ Successfully reached login reward screen.")

            # Backup account data
            success, backup_filename = backup_account_data(adb_address, guest_name, log_func)
            
            if success:
                # Save metadata
                save_account_metadata({
                    "guest_name": guest_name,
                    "backup_file": backup_filename,
                    "login_day": 1,
                    "last_login": datetime.now().strftime("%Y-%m-%d"),
                    "status": "Active"
                })

                valid_instances.append(adb_address)
                valid_guest_names.append(guest_name)
        else:
            log_func(f"[{adb_address}] ❌ Failed to reach reward screen. Closing and deleting.")

            # Cleanup screenshots
            for day_file in os.listdir(SCREENSHOT_DIR):
                if day_file.startswith(adb_address):
                    try:
                        os.remove(os.path.join(SCREENSHOT_DIR, day_file))
                    except Exception as e:
                        pass
            
            for day_file in os.listdir(SCREENSHOT_DIR_FINAL):
                if day_file.startswith(adb_address):
                    try:
                        os.remove(os.path.join(SCREENSHOT_DIR_FINAL, day_file))
                    except Exception as e:
                        pass

            quit_game(adb_address)
            time.sleep(5)

    return valid_instances, valid_guest_names
