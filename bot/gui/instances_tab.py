"""Instance status tab with modern design"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import json
import os

from utils.file_manager import extract_account_data, get_persistent_path

# from account_extract import extract_account


BATCHES_FILE = get_persistent_path('batches.json') 

class InstancesTab:
    """Modern instance status manager"""
    
    def __init__(self, parent):
        """Initialize instances tab"""
        self.frame = ttk.Frame(parent, padding=15)
        self.tree = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create widgets with modern design"""
        # Header
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=X, pady=(0, 15))
        
        ttk.Label(
            header_frame,
            text="📋 Instance Status Monitor",
            font=("Segoe UI", 18, "bold"),
            bootstyle="primary"
        ).pack(side=LEFT)
        
        # Stats Card
        stats_frame = ttk.Frame(self.frame)
        stats_frame.pack(fill=X, pady=(0, 15))
        
        self.stats_labels = {}
        stats = [
            ("Total Accounts", "0", "info"),
            ("Active Today", "0", "success"),
            ("Inactive", "0", "warning")
        ]
        
        for label, value, style in stats:
            card = ttk.Frame(stats_frame, bootstyle=style)
            card.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)
            
            value_label = ttk.Label(
                card,
                text=value,
                font=("Segoe UI", 24, "bold"),
                bootstyle=style
            )
            value_label.pack(pady=(10, 0))
            
            ttk.Label(
                card,
                text=label,
                font=("Segoe UI", 9),
                bootstyle=f"{style}"
            ).pack(pady=(0, 10))
            
            self.stats_labels[label] = value_label
        
        # Treeview Card
        tree_card = ttk.Labelframe(
            self.frame,
            text="Account Details",
            padding=10,
            bootstyle="primary"
        )
        tree_card.pack(fill=BOTH, expand=YES, pady=(0, 15))
        
        # Modern Treeview
        columns = ("Instance Name", "Login Day", "Last Login", "Status")
        self.tree = ttk.Treeview(
            tree_card,
            columns=columns,
            show="headings",
            height=12,
            bootstyle="info"
        )
        
        # Column configuration
        self.tree.heading("Instance Name", text="🏷️ Instance")
        self.tree.heading("Login Day", text="📅 Day")
        self.tree.heading("Last Login", text="🕐 Last Login")
        self.tree.heading("Status", text="📊 Status")
        
        for col in columns:
            self.tree.column(col, anchor=CENTER, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_card, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Control Buttons
        self._create_buttons()
        
        # Load data
        self.refresh()
    
    def _create_buttons(self):
        """Create control buttons"""
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=X)
        
        ttk.Button(
            btn_frame,
            text="🔄 Refresh",
            command=self.refresh,
            bootstyle="info-outline",
            width=15
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="📦 Extract Account",
            command=self.extract_account,
            bootstyle="success-outline",
            width=15
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Delete Account",
            command=self.delete_account,
            bootstyle="danger-outline",
            width=15
        ).pack(side=LEFT, padx=5)
    
    def refresh(self):
        """Reload data"""
        self.tree.delete(*self.tree.get_children())
        
        if not os.path.exists(BATCHES_FILE):
            messagebox.showwarning("Warning", "No batches file found.")
            return
        
        try:
            with open(BATCHES_FILE, "r", encoding="utf-8") as f:
                accounts = json.load(f)
            
            # Update stats
            total = len(accounts)
            active = sum(1 for acc in accounts if acc.get("status") == "Active")
            inactive = total - active
            
            # Update stat labels
            self.stats_labels["Total Accounts"].config(text=str(total))
            self.stats_labels["Active Today"].config(text=str(active))
            self.stats_labels["Inactive"].config(text=str(inactive))
            
            # Insert data with tags for coloring
            for acc in accounts:
                tag = "active" if acc.get("status") == "Active" else "inactive"
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        acc["instance_name"],
                        acc["login_day"],
                        acc["last_login"],
                        acc["status"]
                    ),
                    tags=(tag,)
                )
            
            # Configure tags
            self.tree.tag_configure("active", background="#2d5016", foreground="white")
            self.tree.tag_configure("inactive", background="#501616", foreground="white")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data:\n{e}")
    
    def extract_account(self):
        """Extract selected Chaos Zero Nightmare account"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an account.")
            return

        values = self.tree.item(selected[0], "values")
        instance_name = values[0]

        try:
            with open(BATCHES_FILE, "r", encoding="utf-8") as f:
                accounts = json.load(f)

            account = next((a for a in accounts if a["instance_name"] == instance_name), None)
            if not account:
                messagebox.showerror("Error", f"Account {instance_name} not found.")
                return

            extract_account_data(account, log_func=print)

            messagebox.showinfo("Success", f"Extracted {instance_name} successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract:\n{e}")
    
    def delete_account(self):
        """Delete selected account from list"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an account.")
            return
        
        if not messagebox.askyesno("Confirm", "Delete this account from the list?"):
            return
        
        values = self.tree.item(selected[0], "values")
        instance_name = values[0]
        
        try:
            with open(BATCHES_FILE, "r", encoding="utf-8") as f:
                accounts = json.load(f)
            
            accounts = [a for a in accounts if a["instance_name"] != instance_name]
            
            with open(BATCHES_FILE, "w", encoding="utf-8") as f:
                json.dump(accounts, f, indent=2)
            
            self.refresh()
            messagebox.showinfo("Success", "Account removed from list.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete:\n{e}")
    
    def get_frame(self):
        """Return frame"""
        return self.frame