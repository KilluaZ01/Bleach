"""Main bot control tab for VMOS cloud devices"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, scrolledtext
import threading

from workflows.vmos_manager import VMOSManager

class MainTab:
    """Handles the Main Bot tab functionality for VMOS devices"""
    
    def __init__(self, parent, pause_event, device_manager):
        """Initialize the main tab"""
        self.frame = ttk.Frame(parent, padding=15)
        self.pause_event = pause_event
        self.device_manager = device_manager
        self.vmos_manager = VMOSManager(self.log)
        self.selected_devices = []
        self.cycles_entry = None
        self.device_listbox = None
        self.btn_start = None
        self.btn_pause = None
        self.btn_stop = None
        self.log_area = None
        self.is_running = False
        
        self._create_widgets()
        self._refresh_device_list()
    
    def _create_widgets(self):
        """Create all widgets with modern styling"""
        # Header with icon and title
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="🎮 Chaos Zero Nightmare",
            font=("Segoe UI", 24, "bold"),
            bootstyle="primary"
        ).pack()
        
        ttk.Label(
            header_frame,
            text="VMOS Cloud Device Automation System",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        ).pack()
        
        # Device Selection Card
        device_card = ttk.Labelframe(
            self.frame,
            text="📱 Device Selection",
            padding=20,
            bootstyle="primary"
        )
        device_card.pack(fill=X, pady=(0, 15))
        
        self._create_device_selection(device_card)
        
        # Configuration Card
        config_card = ttk.Labelframe(
            self.frame,
            text="⚙ Automation Configuration",
            padding=20,
            bootstyle="info"
        )
        config_card.pack(fill=X, pady=(0, 15))
        
        self._create_config_fields(config_card)
        
        # Control Buttons
        self._create_control_buttons()
        
        # Log Card
        log_card = ttk.Labelframe(
            self.frame,
            text="📋 Activity Log",
            padding=10,
            bootstyle="success"
        )
        log_card.pack(fill=BOTH, expand=YES, pady=(15, 0))
        
        # Log Area with modern styling
        self.log_area = scrolledtext.ScrolledText(
            log_card,
            width=80,
            height=12,
            font=("Consolas", 9),
            bg="#1a1a1a",
            fg="#00ff00",
            insertbackground="#00ff00",
            relief="flat",
            wrap='word'
        )
        self.log_area.pack(fill=BOTH, expand=YES)
        self.log_area.configure(state='disabled')
    
    def _create_device_selection(self, parent):
        """Create device selection interface"""
        # Instructions
        ttk.Label(
            parent,
            text="📋 Select devices to run automation on:",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor=W, pady=(0, 10))
        
        # Device selection frame
        selection_frame = ttk.Frame(parent)
        selection_frame.pack(fill=BOTH, expand=YES)
        
        # Device listbox with checkboxes (using Treeview)
        self.device_tree = ttk.Treeview(
            selection_frame,
            columns=("name", "adb", "status"),
            show="tree headings",
            height=6,
            selectmode="none"
        )
        
        # Configure columns
        self.device_tree.heading("#0", text="✓")
        self.device_tree.heading("name", text="Device Name")
        self.device_tree.heading("adb", text="ADB Address")
        self.device_tree.heading("status", text="Status")
        
        self.device_tree.column("#0", width=30, minwidth=30)
        self.device_tree.column("name", width=150)
        self.device_tree.column("adb", width=120)
        self.device_tree.column("status", width=80)
        
        # Scrollbar for device tree
        device_scrollbar = ttk.Scrollbar(selection_frame, orient="vertical", command=self.device_tree.yview)
        self.device_tree.configure(yscrollcommand=device_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.device_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        device_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Bind click event for checkbox functionality
        self.device_tree.bind("<Button-1>", self._on_device_click)
        
        # Device action buttons
        device_btn_frame = ttk.Frame(parent)
        device_btn_frame.pack(fill=X, pady=(10, 0))
        
        ttk.Button(
            device_btn_frame,
            text="🔄 Refresh Devices",
            command=self._refresh_device_list,
            bootstyle="info-outline",
            width=20
        ).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(
            device_btn_frame,
            text="☑ Select All",
            command=self._select_all_devices,
            bootstyle="success-outline",
            width=15
        ).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(
            device_btn_frame,
            text="☐ Clear All",
            command=self._clear_all_devices,
            bootstyle="warning-outline",
            width=15
        ).pack(side=LEFT)
    
    def _create_config_fields(self, parent):
        """Create configuration fields"""
        # Cycles configuration
        cycles_frame = ttk.Frame(parent)
        cycles_frame.pack(fill=X, pady=5)
        
        ttk.Label(
            cycles_frame,
            text="🔄 Number of Cycles:",
            font=("Segoe UI", 10),
            width=20,
            anchor=W
        ).pack(side=LEFT)
        
        self.cycles_entry = ttk.Entry(
            cycles_frame,
            font=("Segoe UI", 10),
            bootstyle="info",
            width=10
        )
        self.cycles_entry.insert(0, "1")
        self.cycles_entry.pack(side=RIGHT)
        
        # Info label
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill=X, pady=(10, 0))
        
        ttk.Label(
            info_frame,
            text="ℹ️ Batch size = Number of selected devices | Each cycle runs automation on all selected devices",
            font=("Segoe UI", 9),
            bootstyle="secondary",
            wraplength=500
        ).pack()
    
    def _create_control_buttons(self):
        """Create modern control buttons"""
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=X, pady=15)
        
        # Start Button
        self.btn_start = ttk.Button(
            button_frame,
            text="▶ Start Automation",
            command=self.start_bot,
            bootstyle="success",
            width=20
        )
        self.btn_start.pack(side=LEFT, padx=5, expand=YES)
        
        # Pause/Resume Button
        self.btn_pause = ttk.Button(
            button_frame,
            text="⏸ Pause",
            command=self.toggle_pause,
            bootstyle="warning",
            width=20,
            state=DISABLED
        )
        self.btn_pause.pack(side=LEFT, padx=5, expand=YES)
        
        # Stop Button
        self.btn_stop = ttk.Button(
            button_frame,
            text="⏹ Stop",
            command=self.stop_bot,
            bootstyle="danger",
            width=20,
            state=DISABLED
        )
        self.btn_stop.pack(side=LEFT, padx=5, expand=YES)
    
    def _refresh_device_list(self):
        """Refresh the device list from device manager"""
        # Clear existing items
        for item in self.device_tree.get_children():
            self.device_tree.delete(item)
        
        # Get devices from device manager
        devices = self.device_manager.get_devices()
        
        if not devices:
            self.log("⚠️ No devices found. Please add devices in the Device Manager tab.")
            return
        
        # Add devices to tree
        for i, device in enumerate(devices):
            # Insert with unchecked state
            item_id = self.device_tree.insert(
                "", "end",
                text="☐",  # Unchecked checkbox
                values=(device.get("name", ""), device.get("adb", ""), "Ready"),
                tags=("unchecked",)
            )
            
        self.log(f"📱 Loaded {len(devices)} devices")
    
    def _on_device_click(self, event):
        """Handle device selection clicks"""
        if self.is_running:
            return  # Don't allow selection changes while running
            
        item = self.device_tree.identify_row(event.y)
        if item:
            column = self.device_tree.identify_column(event.x)
            if column == "#0":  # Clicked on checkbox column
                self._toggle_device_selection(item)
    
    def _toggle_device_selection(self, item):
        """Toggle device selection state"""
        current_text = self.device_tree.item(item, "text")
        
        if current_text == "☐":  # Currently unchecked
            self.device_tree.item(item, text="☑", tags=("checked",))
        else:  # Currently checked
            self.device_tree.item(item, text="☐", tags=("unchecked",))
        
        self._update_selected_devices()
    
    def _select_all_devices(self):
        """Select all devices"""
        if self.is_running:
            return
            
        for item in self.device_tree.get_children():
            self.device_tree.item(item, text="☑", tags=("checked",))
        
        self._update_selected_devices()
    
    def _clear_all_devices(self):
        """Clear all device selections"""
        if self.is_running:
            return
            
        for item in self.device_tree.get_children():
            self.device_tree.item(item, text="☐", tags=("unchecked",))
        
        self._update_selected_devices()
    
    def _update_selected_devices(self):
        """Update the list of selected devices"""
        self.selected_devices = []
        devices = self.device_manager.get_devices()
        
        for item in self.device_tree.get_children():
            if self.device_tree.item(item, "text") == "☑":
                values = self.device_tree.item(item, "values")
                device_name = values[0]
                
                # Find the full device data
                for device in devices:
                    if device.get("name") == device_name:
                        self.selected_devices.append(device)
                        break
        
        self.log(f"📋 Selected {len(self.selected_devices)} devices")
    
    def get_config(self):
        """Get bot configuration"""
        return {
            'selected_devices': self.selected_devices,
            'cycles': int(self.cycles_entry.get() or 1),
            'batch_size': len(self.selected_devices)
        }
    
    def validate_config(self):
        """Validate configuration"""
        try:
            config = self.get_config()
            
            if not config['selected_devices']:
                raise ValueError("Please select at least one device.")
            
            if config['cycles'] < 1:
                raise ValueError("Number of cycles must be at least 1.")
            
            return True, config
        except ValueError as e:
            messagebox.showerror("Invalid Configuration", str(e))
            return False, None
    
    def start_bot(self):
        """Start the bot"""
        valid, config = self.validate_config()
        if not valid:
            return
        
        self.is_running = True
        
        # IMPORTANT: Make sure pause event starts cleared (not paused)
        self.pause_event.clear()  # Start in unpaused state
        
        self.btn_start.config(state=DISABLED)
        self.btn_pause.config(state=NORMAL, text="⏸ Pause")  # Reset pause button text
        self.btn_stop.config(state=NORMAL)
        
        self.log("🚀 Starting automation...")
        self.log(f"📱 Running on {len(config['selected_devices'])} devices")
        self.log(f"🔄 Cycles: {config['cycles']}")
        
        threading.Thread(
            target=self._run_bot,
            args=(config,),
            daemon=True
        ).start()
    
    def _run_bot(self, config):
        """Run the bot with VMOS devices"""
        try:
            # Use VMOS manager to handle device automation
            success = self.vmos_manager.run_automation(
                config['selected_devices'],
                config['cycles'],
                self.pause_event,
                lambda: self.is_running,
                self._update_device_status
            )
            
            if success:
                self.log("✅ Automation completed successfully!")
            else:
                self.log("⚠️ Automation completed with some issues.")
                
        except Exception as e:
            self.log(f"❌ Error: {e}")
        finally:
            self.is_running = False
            self.btn_start.config(state=NORMAL)
            self.btn_pause.config(state=DISABLED)
            self.btn_stop.config(state=DISABLED)
            
            # Reset device statuses
            for device in config['selected_devices']:
                self._update_device_status(device['name'], "Ready")
    
    def _update_device_status(self, device_name, status):
        """Update device status in the tree"""
        for item in self.device_tree.get_children():
            values = self.device_tree.item(item, "values")
            if values[0] == device_name:
                new_values = (values[0], values[1], status)
                self.device_tree.item(item, values=new_values)
                break
    
    def toggle_pause(self):
        """Toggle pause state"""
        if self.pause_event.is_set():
            self.pause_event.clear()  # Clear = Resume (not paused)
            self.btn_pause.config(text="⏸ Pause")
            self.log("▶ Automation resumed")
        else:
            self.pause_event.set()    # Set = Paused
            self.btn_pause.config(text="▶ Resume")
            self.log("⏸ Automation paused")
    
    def stop_bot(self):
        """Stop the bot"""
        self.is_running = False
        self.pause_event.clear()  # Clear pause if set
        
        self.log("⏹ Stopping automation...")
        
        # Disconnect all connected devices
        self.vmos_manager.cleanup_connections()
        
        # Reset UI
        self.btn_start.config(state=NORMAL)
        self.btn_pause.config(state=DISABLED, text="⏸ Pause")
        self.btn_stop.config(state=DISABLED)
        
        # Reset device statuses
        for item in self.device_tree.get_children():
            values = self.device_tree.item(item, "values")
            new_values = (values[0], values[1], "Ready")
            self.device_tree.item(item, values=new_values)
    
    def log(self, message):
        """Write to log"""
        if self.log_area:
            self.log_area.configure(state='normal')
            self.log_area.insert('end', f"{message}\n")
            self.log_area.see('end')
            self.log_area.configure(state='disabled')
    
    def get_frame(self):
        """Return the frame"""
        return self.frame