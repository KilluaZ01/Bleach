"""VMOS Device Automation - Handles automation tasks using game progression steps"""

import subprocess
import time
import threading

from utils.file_manager import push_assets

from macros.game_actions import launch_game, clear_game

from .account_setup import validate_accounts
from .game_progression import get_game_steps, execute_macro_steps


class VMOSDeviceAutomation:
    """Handles automation tasks on VMOS devices using existing game progression"""
    
    def __init__(self, log_func):
        """Initialize device automation"""
        self.log = log_func
    
    def run_device_automation(self, device, guest_name="Joe", luck_key=""):
        """Run automation on a connected device using game progression steps"""
        device_name = device.get('name', 'Unknown')
        raw = device.get('adb', '')
        adb_address = raw.replace('adb connect ', '').strip()
        
        self.log(f"🎮 Starting automation on {device_name}")
        
        try:
            clear_game(adb_address)

            push_assets(adb_address)

            launch_game(adb_address)
            time.sleep(60)

            
            # Get game progression steps
            steps = get_game_steps()
            
            # Prepare guest data in the format expected by execute_macro_steps
            # Format: [(device_identifier, guest_name, luck_key)]
            guest_data = [(adb_address, guest_name, luck_key)]
            
            # Create a pause event for this device
            pause_event = threading.Event()
            pause_event.set()  # Start unpaused
            
            # Execute the macro steps
            execute_macro_steps(
                guest_data=guest_data,
                steps=steps,
                log_func=lambda msg: self.log(f"[{device_name}] {msg}"),
                pause_event=pause_event
            )

            validate_accounts(guest_data, lambda msg: self.log(f"[{device_name}] {msg}"))
            
            self.log(f"🎯 [{device_name}] Game automation completed successfully")
            
        except subprocess.TimeoutExpired:
            raise Exception("Device command timeout")
        except Exception as e:
            raise Exception(f"Automation failed: {str(e)}")