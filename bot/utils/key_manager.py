"""Luck Key Manager - Handles distribution of luck keys to devices"""

from utils.paths import LUCK_KEYS

class LuckKeyManager:
    """Manages distribution of unique luck keys to devices"""
    
    def __init__(self):
        """Initialize luck key manager"""
        self.used_keys = set()
        self.available_keys = LUCK_KEYS.copy()
    
    def get_luck_key_for_device(self, device_name):
        """Get a unique luck key for a device
        
        Args:
            device_name: Name of the device
            
        Returns:
            str: Luck key or empty string if none available
        """
        # Check if we have any available keys
        for key in self.available_keys:
            if key not in self.used_keys:
                self.used_keys.add(key)
                return key
        
        # No keys available
        return ""
    
    def release_key(self, luck_key):
        """Release a luck key back to available pool
        
        Args:
            luck_key: The key to release
        """
        if luck_key in self.used_keys:
            self.used_keys.remove(luck_key)
    
    def release_all_keys(self):
        """Release all keys back to available pool"""
        self.used_keys.clear()
    
    def get_available_keys_count(self):
        """Get count of available keys"""
        return len(LUCK_KEYS) - len(self.used_keys)
    
    def get_used_keys_count(self):
        """Get count of used keys"""
        return len(self.used_keys)