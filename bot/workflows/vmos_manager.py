"""VMOS Manager - Fixed pause event logic"""

from random import randint
import threading
import time

from utils.connection_manager import VMOSConnectionManager
from utils.key_manager import LuckKeyManager

from .device_automation import VMOSDeviceAutomation

class VMOSManager:
    """Main VMOS manager that orchestrates connections and uses existing automation"""
    
    def __init__(self, log_func):
        """Initialize VMOS Manager"""
        self.log = log_func
        self.connection_manager = VMOSConnectionManager(log_func)
        self.device_automation = VMOSDeviceAutomation(log_func)
        self.luck_key_manager = LuckKeyManager()
    
    def run_automation(self, selected_devices, cycles, pause_event, is_running_func, status_update_func):
        """Run automation on selected devices using existing game progression"""
        success = True
        device_luck_keys = {}  # Track which device got which luck key
        
        try:
            # Log luck key availability
            total_devices = len(selected_devices)
            available_keys = self.luck_key_manager.get_available_keys_count()
            self.log(f"🔑 Luck Keys: {available_keys} available for {total_devices} devices")
            
            guest_list = ["Alph", "Brav", "Char", "Delt", "Echo", "Fot",
                  "Golf", "Hote", "Indi", "Juli", "Kilo", "Lima"]
    
            guest_name = f"{guest_list[randint(0, len(guest_list) - 1)]}{randint(100, 999)}"


            if total_devices > available_keys:
                self.log(f"⚠️ Warning: {total_devices - available_keys} devices will run without luck keys")
            
            for cycle in range(1, cycles + 1):
                if not is_running_func():
                    break
                    
                self.log(f"🔄 Starting Cycle {cycle}/{cycles}")
                
                # Assign luck keys to devices for this cycle
                if cycle == 1:  # Only assign keys on first cycle
                    self._assign_luck_keys(selected_devices, device_luck_keys)
                
                # Connect to all devices first
                connected_devices = []
                for device in selected_devices:
                    if not is_running_func():
                        break
                    
                    device_name = device.get('name', 'Unknown')
                    status_update_func(device_name, "Connecting")
                    
                    if self.connection_manager.connect_to_device(device):
                        connected_devices.append(device)
                        status_update_func(device_name, "Connected")
                        self.log(f"✅ [{device_name}] Connection successful, proceeding to automation...")
                    else:
                        status_update_func(device_name, "Connection Failed")
                        success = False
                
                # Run automation on connected devices
                for device_index, device in enumerate(connected_devices, 1):
                    if not is_running_func():
                        self.log("🛑 Automation stopped by user")
                        break
                    
                    # Check if paused (FIXED LOGIC)
                    while pause_event.is_set() and is_running_func():
                        self.log(f"⏸️ Automation paused, waiting to resume...")
                        time.sleep(0.5)  # Slightly longer sleep for better responsiveness
                    
                    if not is_running_func():
                        self.log("🛑 Automation stopped by user")
                        break
                    
                    device_name = device.get('name', 'Unknown')
                    luck_key = device_luck_keys.get(device_name, "")
                    
                    self.log(f"🚀 Starting automation on device {device_index}/{len(connected_devices)}: {device_name}")
                    if luck_key:
                        self.log(f"🔑 [{device_name}] Using luck key: {luck_key}")
                    else:
                        self.log(f"🚫 [{device_name}] No luck key available")
                    
                    status_update_func(device_name, "Running")
                    
                    try:
                        # Use your existing game progression system
                        self.device_automation.run_device_automation(
                            device=device,
                            guest_name=guest_name,
                            luck_key=luck_key
                        )
                        
                        status_update_func(device_name, "Completed")
                        self.log(f"✅ Completed device: {device_name}")
                        
                    except Exception as e:
                        status_update_func(device_name, "Error")
                        self.log(f"❌ Error on device {device_name}: {e}")
                        success = False
                
                # Disconnect devices after cycle
                for device in connected_devices:
                    device_name = device.get('name', 'Unknown')
                    self.connection_manager.disconnect_device(device_name)
                    status_update_func(device_name, "Disconnected")
                
                if cycle < cycles and is_running_func():
                    self.log(f"⏳ Cycle {cycle} completed. Preparing for next cycle...")
                    time.sleep(2)
            
            return success
            
        except Exception as e:
            self.log(f"❌ Automation error: {str(e)}")
            return False
        finally:
            # Release all luck keys when automation is complete
            self._release_all_luck_keys(device_luck_keys)
            self.cleanup_connections()
    
    def _assign_luck_keys(self, selected_devices, device_luck_keys):
        """Assign unique luck keys to devices"""
        self.log("🔑 Assigning luck keys to devices...")
        
        for device in selected_devices:
            device_name = device.get('name', 'Unknown')
            luck_key = self.luck_key_manager.get_luck_key_for_device(device_name)
            
            if luck_key:
                device_luck_keys[device_name] = luck_key
                self.log(f"✅ [{device_name}] Assigned luck key: {luck_key}")
            else:
                device_luck_keys[device_name] = ""
                self.log(f"⚠️ [{device_name}] No luck key available")
        
        # Log summary
        keys_assigned = len([k for k in device_luck_keys.values() if k])
        keys_none = len([k for k in device_luck_keys.values() if not k])
        self.log(f"📊 Luck key assignment complete: {keys_assigned} assigned, {keys_none} without keys")
    
    def _release_all_luck_keys(self, device_luck_keys):
        """Release all luck keys back to available pool"""
        self.log("🔓 Releasing all luck keys...")
        
        for device_name, luck_key in device_luck_keys.items():
            if luck_key:
                self.luck_key_manager.release_key(luck_key)
                self.log(f"🔓 [{device_name}] Released luck key: {luck_key}")
        
        device_luck_keys.clear()
        self.log("✅ All luck keys released")
    
    def cleanup_connections(self):
        """Clean up all connections"""
        self.connection_manager.cleanup_all_connections()
    
    def get_connected_devices(self):
        """Get list of currently connected devices"""
        return self.connection_manager.get_connected_devices()
    
    def is_device_connected(self, device_name):
        """Check if a device is connected"""
        return self.connection_manager.is_device_connected(device_name)
    
    def get_luck_key_status(self):
        """Get current luck key status"""
        from utils.paths import LUCK_KEYS
        return {
            'total_keys': len(LUCK_KEYS),
            'available_keys': self.luck_key_manager.get_available_keys_count(),
            'used_keys': self.luck_key_manager.get_used_keys_count(),
            'keys_list': LUCK_KEYS
        }
