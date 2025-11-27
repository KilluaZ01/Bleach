"""Main application window with ttkbootstrap"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading

from .device_manager_tab import DeviceManagerTab
from .main_tab import MainTab
from .instances_tab import InstancesTab
from .daily_tab import DailyTab


class BotGUI(ttk.Window):
    """Modern main window"""
    
    def __init__(self):
        super().__init__(
            title="Silver and Blood Bot",
            themename="darkly",  # Modern dark theme
            size=(900, 700),
            resizable=(True, True)
        )
        
        # Center window
        self.place_window_center()
        
        # Pause event
        self.pause_event = threading.Event()
        self.pause_event.set()
        
        # Create UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI"""
        # Create notebook with modern tabs
        self.notebook = ttk.Notebook(self, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Create tabs
        self.device_manager_tab = DeviceManagerTab(self.notebook)
        self.main_tab = MainTab(self.notebook, self.pause_event, self.device_manager_tab)
        self.instances_tab = InstancesTab(self.notebook)
        self.daily_tab = DailyTab(self.notebook, self.log)

        
        # Add tabs
        self.notebook.add(self.main_tab.get_frame(), text="  😍 Main Bot  ")
        self.notebook.add(self.instances_tab.get_frame(), text="  📋 Instances  ")
        self.notebook.add(self.daily_tab.get_frame(), text="  🕐 Daily Rewards  ")
        self.notebook.add(self.device_manager_tab.get_frame(), text="  🤤 Device Manager")

        
        # Status bar
        self._create_status_bar()
    
    def _create_status_bar(self):
        """Create status bar"""
        status_frame = ttk.Frame(self, bootstyle="secondary")
        status_frame.pack(fill=X, side=BOTTOM)
        
        ttk.Label(
            status_frame,
            text="🎮 Chaos Zero Nightmare",
            font=("Segoe UI", 8),
            bootstyle="secondary"
        ).pack(side=LEFT, padx=10, pady=3)
        
        ttk.Label(
            status_frame,
            text="Ready",
            font=("Segoe UI", 8),
            bootstyle="success"
        ).pack(side=RIGHT, padx=10, pady=3)
    
    def log(self, message):
        """Log message"""
        self.main_tab.log(message)