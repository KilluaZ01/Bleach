"""VMOS Device Automation - Handles automation tasks using game progression steps"""

import subprocess
import time
import threading

from utils.file_manager import push_assets

from macros.game_actions import launch_game, uninstall_game

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
            uninstall_game(adb_address)

            # push_assets(adb_address)

            launch_game(adb_address)
            time.sleep(50)

            
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

    def _run_single_device_automation(self, device, guest_name, luck_key, results, device_index):
        """Internal method to run automation on a single device (for threading)"""
        device_name = device.get('name', 'Unknown')
        try:
            self.run_device_automation(device, guest_name, luck_key)
            results[device_index] = {'success': True, 'device': device_name, 'error': None}
        except Exception as e:
            results[device_index] = {'success': False, 'device': device_name, 'error': str(e)}

    def run_synchronized_device_automation(self, devices, guest_names=None, luck_keys=None, pause_event=None):
        """Run automation on multiple devices with synchronized step execution
        
        This method executes each step simultaneously across all devices:
        1. All devices clear game data together
        2. All devices launch game together  
        3. All devices execute each macro step together
        
        Args:
            devices: List of device dictionaries
            guest_names: List of guest names (one per device) or single name for all
            luck_keys: Dictionary of device_name -> luck_key or list of keys
            pause_event: Threading event for pause control
            
        Returns:
            dict: Results summary with success/failure info for each device
        """
        if not devices:
            self.log("❌ No devices provided for automation")
            return {'success': False, 'results': {}}
        
        # Prepare guest names
        if guest_names is None:
            guest_names = ["Joe"] * len(devices)
        elif isinstance(guest_names, str):
            guest_names = [guest_names] * len(devices)
        elif len(guest_names) < len(devices):
            last_name = guest_names[-1] if guest_names else "Joe"
            guest_names.extend([last_name] * (len(devices) - len(guest_names)))
        
        # Prepare luck keys
        if luck_keys is None:
            luck_keys = [""] * len(devices)
        elif isinstance(luck_keys, dict):
            luck_keys = [luck_keys.get(device.get('name', ''), "") for device in devices]
        elif isinstance(luck_keys, str):
            luck_keys = [luck_keys] * len(devices)
        elif len(luck_keys) < len(devices):
            luck_keys.extend([""] * (len(devices) - len(luck_keys)))
        
        # Create pause event if not provided
        if pause_event is None:
            pause_event = threading.Event()
            pause_event.set()  # Start unpaused
        
        self.log(f"🚀 Starting synchronized automation on {len(devices)} devices")
        
        # Extract ADB addresses and prepare guest data
        guest_data = []
        device_info = {}  # For tracking device info
        
        for i, device in enumerate(devices):
            device_name = device.get('name', f'Unknown-{i}')
            raw = device.get('adb', '')
            adb_address = raw.replace('adb connect ', '').strip()
            guest_name = guest_names[i]
            luck_key = luck_keys[i]
            
            guest_data.append((adb_address, guest_name, luck_key))
            device_info[adb_address] = device_name
            
            self.log(f"🔧 [{device_name}] Prepared for synchronized automation")
            if luck_key:
                self.log(f"🔑 [{device_name}] Using luck key: {luck_key}")
            else:
                self.log(f"🚫 [{device_name}] No luck key available")
        
        try:
            # Step 1: Uninstall game on all devices simultaneously
            # self.log("🧹 Step 1: Uninstalling game on all devices...")
            # uninstall_threads = []
            # for adb_address, _, _ in guest_data:
            #     thread = threading.Thread(target=uninstall_game, args=(adb_address,))
            #     uninstall_threads.append(thread)
            #     thread.start()
            
            # for thread in uninstall_threads:
            #     thread.join()
            
            # # Step 1.5: Reinstall game on all devices simultaneously
            # self.log("🧹 Step 1.5: Reinstalling game on all devices...")
            # reinstall_threads = []
            # for adb_address, _, _ in guest_data:
            #     thread = threading.Thread(target=uninstall_game, args=(adb_address,))
            #     reinstall_threads.append(thread)
            #     thread.start()
            
            # for thread in reinstall_threads:
            #     thread.join()
            
            # Step 2: Launch game on all devices simultaneously
            self.log("🎮 Step 2: Launching game on all devices...")
            launch_threads = []
            for adb_address, _, _ in guest_data:
                thread = threading.Thread(target=launch_game, args=(adb_address,))
                launch_threads.append(thread)
                thread.start()
            
            for thread in launch_threads:
                thread.join()
            
            time.sleep(50)  # Wait for all games to load
            
            # Step 3: Execute macro steps synchronously using existing system
            self.log("🎯 Step 3: Executing macro steps synchronously...")
            steps = get_game_steps()
            
            execute_macro_steps(
                guest_data=guest_data,
                steps=steps,
                log_func=self.log,
                pause_event=pause_event
            )
            
            # Step 4: Validate accounts
            self.log("✅ Step 4: Validating accounts...")
            validate_accounts(guest_data, self.log)
            
            # All successful
            successful_devices = [device_info[adb_address] for adb_address, _, _ in guest_data]
            results = {}
            for i, (adb_address, _, _) in enumerate(guest_data):
                device_name = device_info[adb_address]
                results[i] = {'success': True, 'device': device_name, 'error': None}
                self.log(f"🎯 [{device_name}] Synchronized automation completed successfully")
            
            self.log(f"📊 Synchronized Automation Summary:")
            self.log(f"   Total devices: {len(devices)}")
            self.log(f"   ✅ All {len(devices)} devices completed successfully!")
            self.log(f"   🎯 Successful devices: {', '.join(successful_devices)}")
            
            return {
                'success': True,
                'total': len(devices),
                'successful': len(devices),
                'failed': 0,
                'successful_devices': successful_devices,
                'failed_devices': [],
                'results': results
            }
            
        except Exception as e:
            self.log(f"❌ Synchronized automation failed: {str(e)}")
            
            # Mark all as failed
            failed_devices = []
            results = {}
            for i, (adb_address, _, _) in enumerate(guest_data):
                device_name = device_info[adb_address]
                results[i] = {'success': False, 'device': device_name, 'error': str(e)}
                failed_devices.append({'device': device_name, 'error': str(e)})
            
            return {
                'success': False,
                'total': len(devices),
                'successful': 0,
                'failed': len(devices),
                'successful_devices': [],
                'failed_devices': failed_devices,
                'results': results
            }
    
    def run_parallel_device_automation(self, devices, guest_names=None, luck_keys=None):
        """Legacy method - redirects to synchronized automation
        
        Args:
            devices: List of device dictionaries
            guest_names: List of guest names (one per device) or single name for all
            luck_keys: Dictionary of device_name -> luck_key or list of keys
            
        Returns:
            dict: Results summary with success/failure info for each device
        """
        self.log("🔄 Redirecting to synchronized automation for proper step coordination...")
        return self.run_synchronized_device_automation(devices, guest_names, luck_keys)