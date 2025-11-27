"""Device Manager tab for VMOS cloud devices"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from utils.file_manager import get_persistent_path

class DeviceManagerTab:
    def __init__(self, parent):
        self.parent = parent
        self.devices = []
        self.selected_device = None
        
        # Load devices on initialization
        self.load_devices()
        
        # Create the main frame
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the device manager UI"""
        # Main container with padding
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_container, text="Device Manager", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Device list frame
        list_frame = ttk.LabelFrame(main_container, text="Devices", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Treeview for device list
        self.tree = ttk.Treeview(list_frame, columns=("name", "command", "key", "adb"), show="headings", height=8)
        self.tree.heading("name", text="Device Name")
        self.tree.heading("command", text="Connection Command")
        self.tree.heading("key", text="Connection Key")
        self.tree.heading("adb", text="ADB Address")
        
        # Column widths
        self.tree.column("name", width=150)
        self.tree.column("command", width=200)
        self.tree.column("key", width=150)
        self.tree.column("adb", width=150)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_device_select)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_container)
        buttons_frame.pack(fill="x", pady=(0, 10))
        
        # Add Device button
        add_btn = ttk.Button(buttons_frame, text="Add Device", command=self.add_device)
        add_btn.pack(side="left", padx=(0, 5))
        
        # Edit Device button
        edit_btn = ttk.Button(buttons_frame, text="Edit Device", command=self.edit_device)
        edit_btn.pack(side="left", padx=(0, 5))
        
        # Delete Device button
        delete_btn = ttk.Button(buttons_frame, text="Delete Device", command=self.delete_device)
        delete_btn.pack(side="left")
        
        # Device form frame (initially hidden)
        self.form_frame = ttk.LabelFrame(main_container, text="Device Details", padding=10)
        
        # Form fields
        ttk.Label(self.form_frame, text="Device Name:").grid(row=0, column=0, sticky="w", pady=2)
        self.name_entry = ttk.Entry(self.form_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        ttk.Label(self.form_frame, text="Connection Command:").grid(row=1, column=0, sticky="w", pady=2)
        self.command_entry = ttk.Entry(self.form_frame, width=30)
        self.command_entry.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        ttk.Label(self.form_frame, text="Connection Key:").grid(row=2, column=0, sticky="w", pady=2)
        self.key_entry = ttk.Entry(self.form_frame, width=30)
        self.key_entry.grid(row=2, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        ttk.Label(self.form_frame, text="ADB Address:").grid(row=3, column=0, sticky="w", pady=2)
        self.adb_entry = ttk.Entry(self.form_frame, width=30)
        self.adb_entry.grid(row=3, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        # Form buttons
        form_buttons_frame = ttk.Frame(self.form_frame)
        form_buttons_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        self.save_btn = ttk.Button(form_buttons_frame, text="Save", command=self.save_device)
        self.save_btn.pack(side="left", padx=(0, 5))
        
        self.cancel_btn = ttk.Button(form_buttons_frame, text="Cancel", command=self.cancel_form)
        self.cancel_btn.pack(side="left")
        
        # Configure grid weights
        self.form_frame.columnconfigure(1, weight=1)
        
        # Load and display devices
        self.refresh_device_list()
    
    def load_devices(self):
        """Load devices from persistent storage"""
        try:
            devices_file = get_persistent_path("device_data.json")
            if os.path.exists(devices_file):
                with open(devices_file, "r", encoding="utf-8") as f:
                    self.devices = json.load(f)
            else:
                self.devices = []
        except (json.JSONDecodeError, FileNotFoundError):
            self.devices = []
            
    def save_devices(self):
        """Save devices to persistent storage"""
        try:
            devices_file = get_persistent_path("device_data.json")
            with open(devices_file, "w", encoding="utf-8") as f:
                json.dump(self.devices, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save devices: {str(e)}")
            
    def refresh_device_list(self):
        """Refresh the device list in the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add devices to tree
        for device in self.devices:
            self.tree.insert("", "end", values=(
                device.get("name", ""),
                device.get("command", ""),
                device.get("key", ""),
                device.get("adb", "")
            ))
    
    def on_device_select(self, event):
        """Handle device selection in treeview"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item["values"]
            if values:
                # Find the selected device
                for device in self.devices:
                    if (device.get("name") == values[0] and 
                        device.get("command") == values[1] and
                        device.get("key") == values[2] and
                        device.get("adb") == values[3]):
                        self.selected_device = device
                        break
    
    def add_device(self):
        """Show form to add a new device"""
        self.clear_form()
        self.form_frame.pack(fill="x", pady=(10, 0))
        self.selected_device = None
        self.form_frame.configure(text="Add New Device")
        
    def edit_device(self):
        """Edit the selected device"""
        if not self.selected_device:
            messagebox.showwarning("Warning", "Please select a device to edit.")
            return
            
        self.form_frame.pack(fill="x", pady=(10, 0))
        self.form_frame.configure(text="Edit Device")
        
        # Populate form with selected device data
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.selected_device.get("name", ""))
        
        self.command_entry.delete(0, tk.END)
        self.command_entry.insert(0, self.selected_device.get("command", ""))
        
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, self.selected_device.get("key", ""))
        
        self.adb_entry.delete(0, tk.END)
        self.adb_entry.insert(0, self.selected_device.get("adb", ""))
    
    def delete_device(self):
        """Delete the selected device"""
        if not self.selected_device:
            messagebox.showwarning("Warning", "Please select a device to delete.")
            return
            
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete device '{self.selected_device.get('name', 'Unknown')}'?")
        if result:
            self.devices.remove(self.selected_device)
            self.save_devices()
            self.refresh_device_list()
            self.selected_device = None
            messagebox.showinfo("Success", "Device deleted successfully!")
    
    def save_device(self):
        """Save the device from the form"""
        # Validate form fields
        name = self.name_entry.get().strip()
        command = self.command_entry.get().strip()
        command = command.replace("-Nf", "").strip()
        key = self.key_entry.get().strip()
        adb = self.adb_entry.get().strip()
        
        if not all([name, command, key, adb]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Check for duplicate names (except when editing the same device)
        for device in self.devices:
            if (device.get("name") == name and 
                device != self.selected_device):
                messagebox.showerror("Error", "A device with this name already exists!")
                return
        
        # Create device data
        device_data = {
            "name": name,
            "command": command,
            "key": key,
            "adb": adb
        }
        
        if self.selected_device:
            # Update existing device
            index = self.devices.index(self.selected_device)
            self.devices[index] = device_data
        else:
            # Add new device
            self.devices.append(device_data)
        
        # Save and refresh
        self.save_devices()
        self.refresh_device_list()
        self.cancel_form()
        messagebox.showinfo("Success", "Device saved successfully!")
    
    def cancel_form(self):
        """Cancel form editing and hide the form"""
        self.form_frame.pack_forget()
        self.clear_form()
        self.selected_device = None
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, tk.END)
        self.command_entry.delete(0, tk.END)
        self.key_entry.delete(0, tk.END)
        self.adb_entry.delete(0, tk.END)
    
    def get_devices(self):
        """Return the list of devices"""
        return self.devices
    
    def get_device_by_name(self, name):
        """Get device by name"""
        for device in self.devices:
            if device.get("name") == name:
                return device
        return None
    
    def get_frame(self):
        """Return frame"""
        return self.frame