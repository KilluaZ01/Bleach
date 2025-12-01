"""File and data management utilities"""

import os
import json
import subprocess
from datetime import datetime
import time

from utils.paths import ASSETS_DIR, BACKUP_DIR, MAIN_PATH, PACKAGE_NAME

def get_persistent_path(filename, subdir=None):
    """Get persistent file path in AppData
    
    Args:
        filename: Name of the file
        subdir: Optional subdirectory
        
    Returns:
        str: Full file path
    """
    base_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'ChaosZeroNightmare')
    if subdir:
        base_dir = os.path.join(base_dir, subdir)
    os.makedirs(base_dir, exist_ok=True)
    
    file_path = os.path.join(base_dir, filename)
    
    # Create empty batches.json if it doesn't exist
    if filename == "batches.json" and not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)
        print(f"✅ Created empty {filename} at {file_path}")
    
    # Create empty device_data.json if it doesn't exist
    if filename == "device_data.json" and not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)
        print(f"✅ Created empty {filename} at {file_path}")
    
    return file_path

def push_assets(adb_address):
    move_cmd = [
    "adb", "-s", adb_address, "shell",
    "cd /storage/emulated/0/Android/data && tar -xzf /storage/emulated/0/Download/external2.tar.gz"
    ]   

    r1 = subprocess.run(move_cmd)

    if r1.returncode != 0:
        print(f"[{adb_address}] ❌ Failed to move external data.")
        return

    print(f"[{adb_address}] ✅ Successfully pushed external data.")

def save_account_metadata(account):
    """Save account metadata to batches.json
    
    Args:
        account: Dictionary containing account information
    """
    accounts_file = get_persistent_path("batches.json")

    # Load existing accounts
    if os.path.exists(accounts_file):
        with open(accounts_file, "r", encoding="utf-8") as f:
            try:
                all_accounts = json.load(f)
            except json.JSONDecodeError:
                all_accounts = []
    else:
        all_accounts = []

    # Append new account
    all_accounts.append(account)

    # Save back
    with open(accounts_file, "w", encoding="utf-8") as f:
        json.dump(all_accounts, f, indent=2)

    print(f"✅ Account metadata saved for {account['instance_name']}")

def backup_account_data(adb_address, guest_name, log_func):
    """Create and save account backup
    
    Args:
        adb_address: ADB address of the device
        guest_name: Guest account name
        log_func: Logging function
        
    Returns:
        tuple: (success: bool, backup_filename: str)
    """
    account_dir = f"{MAIN_PATH}accounts"
    os.makedirs(account_dir, exist_ok=True)

    safe_guest = guest_name
    ts = datetime.now().strftime("%M%S")

    backup_filename = f"{safe_guest}_{ts}.tar.gz"
    backup_path = os.path.join(account_dir, backup_filename)

    # Create tar backup
    # make_tar_cmd = (
    #     f'ldconsole.exe adb --name "{instance_name}" '
    #     f'--command "shell su -c \'cd /data/data && '
    #     f'tar -czf /sdcard/{backup_filename} com.smilegate.chaoszero.stove.google\'"'
    # )
    
    # pull_tar_cmd = (
    #     f'ldconsole.exe adb --name "{instance_name}" '
    #     f'--command "pull /sdcard/{backup_filename} {backup_path}"'
    # )
    
    # clean_tar_cmd = (
    #     f'ldconsole.exe adb --name "{instance_name}" '
    #     f'--command "shell rm /sdcard/{backup_filename}"'
    # )

    # r1 = subprocess.run(make_tar_cmd, shell=True)
    # if r1.returncode != 0:
    #     log_func(f"[{instance_name}] ❌ Failed to create internal backup tar.")
    #     return False, None
    
    # r2 = subprocess.run(pull_tar_cmd, shell=True)
    # if r2.returncode != 0:
    #     log_func(f"[{instance_name}] ❌ Failed to pull backup from device.")
    #     return False, None
    
    # subprocess.run(clean_tar_cmd, shell=True)
    # log_func(f"[{instance_name}] 💾 Saved internal backup -> {backup_path}")
    
    return True, backup_filename

def extract_account_data(account, log_func=print):
    instance_name = account["instance_name"]
    backup_file = account["backup_file"]
    backup_path = os.path.join(BACKUP_DIR, backup_file)
    base_instance = "Chaos_Base"

    # Clone a new instance 
    log_func(f"Cloned instance: {instance_name}")
    os.system(f'ldconsole.exe copy --name "{instance_name}" --from "{base_instance}"') 
    
    # Launch instance 
    log_func(f"🚀 Launching {instance_name}")
    os.system(f'ldconsole.exe launch --name "{instance_name}"') 
    time.sleep(70)

    os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell pm clear {PACKAGE_NAME}"')
    time.sleep(3)

    push_assets(instance_name)
    time.sleep(2)

    log_func(f"📤 Pushing tar...")
    subprocess.run(
        f'ldconsole.exe adb --name "{instance_name}" '
        f'--command "push {backup_path} /sdcard/"',
        shell=True
    )
    time.sleep(3)

    log_func("📦 Extracting backup...")
    extract_cmd = (
        f'ldconsole.exe adb --name "{instance_name}" '
        f'--command \"shell su -c \'cd /data/data && tar -xzf /sdcard/{backup_file}\'\"'
    )
    subprocess.run(extract_cmd, shell=True)

    log_func("✅ Account restored successfully!")
