"""VMOS Connection Manager - Handles device connections using SSH tunnels"""

import subprocess
import threading
import time
import json
import base64
import sshtunnel
import atexit
from utils.file_manager import get_persistent_path

class VMOSConnectionManager:
    """Manages VMOS cloud device connections using SSH tunnels"""
    
    def __init__(self, log_func):
        """Initialize connection manager"""
        self.log = log_func
        self.connected_devices = {}
        self.ssh_tunnels = {}
        self.connection_lock = threading.Lock()
        # Register cleanup on exit
        atexit.register(self.cleanup_all_connections)
    
    def connect_to_device(self, device):
        """Connect to a VMOS device using SSH tunnel"""
        device_name = device.get('name', 'Unknown')
        connection_command = device.get('command', '')
        connection_key = device.get('key', '')
        adb_address = device.get('adb', '')
        
        if not all([connection_command, connection_key, adb_address]):
            self.log(f"❌ [{device_name}] Missing connection details")
            return False
        
        try:
            with self.connection_lock:
                self.log(f"🔌 [{device_name}] Initiating SSH tunnel connection...")
                
                # Parse connection details from the device info
                ssh_info = self._parse_connection_info(device_name, connection_command, connection_key, adb_address)
                if not ssh_info:
                    return False
                
                # Step 1: Create SSH tunnel
                self.log(f"🔧 [{device_name}] Creating SSH tunnel...")
                tunnel_success = self._create_ssh_tunnel(device_name, ssh_info)
                
                if not tunnel_success:
                    self.log(f"❌ [{device_name}] Failed to establish SSH tunnel")
                    return False
                
                # Step 2: Connect ADB through tunnel
                self.log(f"📱 [{device_name}] Connecting ADB through tunnel...")
                adb_success = self._connect_adb_through_tunnel(device_name, ssh_info)
                
                if not adb_success:
                    self.log(f"❌ [{device_name}] Failed to connect ADB through tunnel")
                    self._cleanup_device_connection(device_name)
                    return False
                
                # Store connection info
                self.connected_devices[device_name] = {
                    'device': device,
                    'ssh_info': ssh_info,
                    'connected_at': time.time()
                }
                
                self.log(f"✅ [{device_name}] Successfully connected via SSH tunnel!")
                return True
                
        except Exception as e:
            self.log(f"❌ [{device_name}] Connection error: {str(e)}")
            self._cleanup_device_connection(device_name)
            return False
    
    def _parse_connection_info(self, device_name, connection_command, connection_key, adb_address):
        """Parse SSH connection information from device data"""
        try:
            # Example connection_command: "ssh -L 5555:adb-proxy:5555 user@host -p 22"
            # We need to extract: user, host, port, and local/remote ports
            
            # For now, let's assume the connection_command contains the SSH details
            # You might need to adjust this parsing based on your actual command format
            
            # Extract host and user from connection command
            if "@" in connection_command and "ssh" in connection_command.lower():
                # Parse SSH command
                parts = connection_command.split()
                
                # Find the user@host part
                user_host = None
                ssh_port = 22  # default
                local_port = 5555  # default
                remote_port = 5555  # default
                
                for i, part in enumerate(parts):
                    if "@" in part:
                        user_host = part
                    elif part == "-p" and i + 1 < len(parts):
                        ssh_port = int(parts[i + 1])
                    elif part == "-L" and i + 1 < len(parts):
                        # Parse port forwarding: local_port:remote_host:remote_port
                        forwarding = parts[i + 1]
                        if ":" in forwarding:
                            port_parts = forwarding.split(":")
                            if len(port_parts) >= 3:
                                local_port = int(port_parts[0])
                                remote_port = int(port_parts[2])
                
                if not user_host:
                    self.log(f"❌ [{device_name}] Could not parse user@host from command")
                    return None
                
                ssh_user, ssh_host = user_host.split("@")
                
                # Decode password if it's base64 encoded
                pwd = connection_key
                try:
                    pwd = base64.b64decode(connection_key).decode("utf-8")
                except Exception:
                    pass  # already plaintext
                
                return {
                    'ssh_user': ssh_user,
                    'ssh_host': ssh_host,
                    'ssh_port': ssh_port,
                    'connection_key': pwd,
                    'local_port': local_port,
                    'remote_port': remote_port,
                    'adb_address': adb_address
                }
            
            else:
                # If not a standard SSH command, try to use the adb_address directly
                # Assume adb_address format is "host:port"
                if ":" in adb_address:
                    host, port = adb_address.split(":", 1)
                    return {
                        'ssh_user': 'unknown',  # You might need to get this from somewhere else
                        'ssh_host': host,
                        'ssh_port': 22,
                        'connection_key': connection_key,
                        'local_port': 5555,
                        'remote_port': int(port),
                        'adb_address': adb_address
                    }
                
        except Exception as e:
            self.log(f"❌ [{device_name}] Error parsing connection info: {str(e)}")
            return None
    
    def _create_ssh_tunnel(self, device_name, ssh_info):
        """Create SSH tunnel for the device"""
        try:
            user = ssh_info['ssh_user']
            host = ssh_info['ssh_host']
            port = ssh_info['ssh_port']
            local_port = ssh_info['local_port']
            remote_port = ssh_info['remote_port']
            pwd = ssh_info['connection_key']
            
            self.log(f"🔗 [{device_name}] {user}@{host}:{port}")
            self.log(f"🔗 [{device_name}] Forwarding localhost:{local_port} -> adb-proxy:{remote_port}")
            
            # Create SSH tunnel
            tunnel = sshtunnel.SSHTunnelForwarder(
                (host, port),
                ssh_username=user,
                ssh_password=pwd,
                remote_bind_address=("adb-proxy", remote_port),
                local_bind_address=("127.0.0.1", local_port),
                set_keepalive=10.0  # Keep connection alive
            )
            
            tunnel.start()
            
            # Store the tunnel
            self.ssh_tunnels[device_name] = tunnel
            
            self.log(f"✅ [{device_name}] SSH tunnel started on localhost:{local_port}")
            time.sleep(1.5)  # Give tunnel time to establish
            
            return True
            
        except Exception as e:
            self.log(f"❌ [{device_name}] Failed to create SSH tunnel: {str(e)}")
            return False
    
    def _connect_adb_through_tunnel(self, device_name, ssh_info):
        """Connect ADB through the SSH tunnel"""
        try:
            local_port = ssh_info['local_port']
            adb_address = f"localhost:{local_port}"
            
            # Disconnect any existing connection
            disconnect_cmd = f"adb disconnect {adb_address}"
            subprocess.run(disconnect_cmd, shell=True, capture_output=True, timeout=10)
            
            # Connect through tunnel
            connect_cmd = f"adb connect {adb_address}"
            self.log(f"📱 [{device_name}] Running: {connect_cmd}")
            
            result = subprocess.run(
                connect_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.log(f"✅ [{device_name}] ADB connected: {adb_address}")
                self.log(f"📱 [{device_name}] {result.stdout.strip()}")
                
                # Verify connection with a test command
                time.sleep(2)
                test_cmd = f"adb -s {adb_address} shell echo 'tunnel_test'"
                test_result = subprocess.run(
                    test_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if test_result.returncode == 0:
                    self.log(f"✅ [{device_name}] ADB tunnel connection verified")
                    # Update ssh_info with the actual ADB address used
                    ssh_info['tunnel_adb_address'] = adb_address
                    return True
                else:
                    self.log(f"⚠️ [{device_name}] ADB connected but test failed")
                    return False
            else:
                self.log(f"❌ [{device_name}] ADB connection failed: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log(f"⏱️ [{device_name}] ADB connection timeout")
            return False
        except Exception as e:
            self.log(f"❌ [{device_name}] ADB connection error: {str(e)}")
            return False
    
    def disconnect_device(self, device_name):
        """Disconnect a device and close its SSH tunnel"""
        if device_name not in self.connected_devices:
            return True
        
        try:
            with self.connection_lock:
                device_info = self.connected_devices[device_name]
                ssh_info = device_info['ssh_info']
                
                # Disconnect ADB
                if 'tunnel_adb_address' in ssh_info:
                    adb_address = ssh_info['tunnel_adb_address']
                    disconnect_cmd = f"adb disconnect {adb_address}"
                    subprocess.run(disconnect_cmd, shell=True, capture_output=True, timeout=10)
                    self.log(f"📱 [{device_name}] ADB disconnected")
                
                # Close SSH tunnel
                if device_name in self.ssh_tunnels:
                    try:
                        self.ssh_tunnels[device_name].stop()
                        del self.ssh_tunnels[device_name]
                        self.log(f"🔐 [{device_name}] SSH tunnel closed")
                    except Exception as e:
                        self.log(f"⚠️ [{device_name}] Error closing SSH tunnel: {str(e)}")
                
                # Remove from connected devices
                del self.connected_devices[device_name]
                self.log(f"🔌 [{device_name}] Disconnected successfully")
                return True
                
        except Exception as e:
            self.log(f"❌ [{device_name}] Error disconnecting: {str(e)}")
            return False
    
    def _cleanup_device_connection(self, device_name):
        """Clean up failed connection attempt"""
        if device_name in self.connected_devices:
            del self.connected_devices[device_name]
        
        # Close SSH tunnel if exists
        if device_name in self.ssh_tunnels:
            try:
                self.ssh_tunnels[device_name].stop()
                del self.ssh_tunnels[device_name]
            except:
                pass
    
    def cleanup_all_connections(self):
        """Clean up all connections and SSH tunnels"""
        self.log("🧹 Cleaning up all device connections and SSH tunnels...")
        
        device_names = list(self.connected_devices.keys())
        for device_name in device_names:
            self.disconnect_device(device_name)
        
        # Clean up any remaining SSH tunnels
        for device_name, tunnel in list(self.ssh_tunnels.items()):
            try:
                tunnel.stop()
            except:
                pass
        
        self.ssh_tunnels.clear()
        self.log("✅ All connections and tunnels cleaned up")
    
    def get_connected_devices(self):
        """Get list of currently connected devices"""
        return self.connected_devices.copy()
    
    def is_device_connected(self, device_name):
        """Check if a device is connected"""
        return device_name in self.connected_devices
    
    def get_tunnel_info(self, device_name):
        """Get tunnel information for a device"""
        if device_name in self.connected_devices:
            return self.connected_devices[device_name]['ssh_info']
        return None