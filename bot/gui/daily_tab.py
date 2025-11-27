"""Daily rewards automation tab"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import subprocess


MAIN_PATH = 'D:/Silver_Blood_Bot/'


class DailyTab:
    """Modern daily rewards manager"""
    
    def __init__(self, parent, log_callback):
        """Initialize daily tab"""
        self.frame = ttk.Frame(parent, padding=15)
        self.log_callback = log_callback
        self.auto_claim_enabled = False
        
        self._create_widgets()
        self._check_initial_state()
    
    def _create_widgets(self):
        """Create widgets with modern design"""
        # Header
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="🕐 Daily Rewards Automation",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack()
        
        ttk.Label(
            header_frame,
            text="Schedule automatic daily login rewards collection",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        ).pack()
        
        # Configuration Card
        config_card = ttk.Labelframe(
            self.frame,
            text="⚙ Schedule Configuration",
            padding=20,
            bootstyle="info"
        )
        config_card.pack(fill=X, pady=(0, 20))
        
        # Time Input
        time_frame = ttk.Frame(config_card)
        time_frame.pack(fill=X, pady=10)
        
        ttk.Label(
            time_frame,
            text="🕐 Auto-Claim Time:",
            font=("Segoe UI", 11),
            width=20,
            anchor=W
        ).pack(side=LEFT)
        
        self.claim_time_entry = ttk.Entry(
            time_frame,
            font=("Segoe UI", 11),
            bootstyle="info",
            width=15
        )
        self.claim_time_entry.insert(0, "09:00")
        self.claim_time_entry.pack(side=LEFT, padx=10)
        
        ttk.Label(
            time_frame,
            text="(HH:MM format)",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack(side=LEFT)
        
        # Batch Size Input
        batch_frame = ttk.Frame(config_card)
        batch_frame.pack(fill=X, pady=10)
        
        ttk.Label(
            batch_frame,
            text="📦 Accounts per Batch:",
            font=("Segoe UI", 11),
            width=20,
            anchor=W
        ).pack(side=LEFT)
        
        self.accounts_per_batch_entry = ttk.Entry(
            batch_frame,
            font=("Segoe UI", 11),
            bootstyle="info",
            width=15
        )
        self.accounts_per_batch_entry.insert(0, "2")
        self.accounts_per_batch_entry.pack(side=LEFT, padx=10)
        
        # Status Card
        status_card = ttk.Labelframe(
            self.frame,
            text="📊 Current Status",
            padding=20,
            bootstyle="success"
        )
        status_card.pack(fill=X, pady=(0, 20))
        
        self.status_label = ttk.Label(
            status_card,
            text="⚪ Auto-Claim: Disabled",
            font=("Segoe UI", 12, "bold"),
            bootstyle="secondary"
        )
        self.status_label.pack(pady=10)
        
        self.schedule_info = ttk.Label(
            status_card,
            text="No schedule configured",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        self.schedule_info.pack()
        
        # Toggle Button
        self.btn_toggle_auto = ttk.Button(
            self.frame,
            text="✅ Enable Daily Auto-Claim",
            command=self.toggle_auto_claim,
            bootstyle="success",
            width=30
        )
        self.btn_toggle_auto.pack(pady=20)
        
        # Info Card
        info_card = ttk.Labelframe(
            self.frame,
            text="ℹ️ Information",
            padding=15,
            bootstyle="secondary"
        )
        info_card.pack(fill=BOTH, expand=YES)
        
        info_text = """
        • Daily auto-claim runs automatically at the scheduled time
        • Make sure the bot executable is in the correct location
        • The task will run even when you're not logged in
        • You can modify the schedule at any time
        • Check Windows Task Scheduler for more options
        """
        
        ttk.Label(
            info_card,
            text=info_text,
            font=("Segoe UI", 9),
            justify=LEFT,
            bootstyle="secondary"
        ).pack(anchor=W)
    
    def _check_initial_state(self):
        """Check task status"""
        if self._task_exists():
            self.auto_claim_enabled = True
            self.btn_toggle_auto.config(
                text="🔴 Disable Daily Auto-Claim",
                bootstyle="danger"
            )
            self.status_label.config(
                text="🟢 Auto-Claim: Enabled",
                bootstyle="success"
            )
            time_str = self.claim_time_entry.get()
            self.schedule_info.config(
                text=f"Scheduled daily at {time_str}"
            )
    
    def _task_exists(self, task_name="SilverBloodAutoClaim"):
        """Check if task exists"""
        result = subprocess.run(
            f'schtasks /Query /TN {task_name}',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    
    def toggle_auto_claim(self):
        """Toggle auto-claim"""
        # Validate inputs
        time_str = self.claim_time_entry.get().strip()
        try:
            hour, minute = map(int, time_str.split(":"))
            if not (0 <= hour < 24 and 0 <= minute < 60):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Time", "Use HH:MM format (00:00 - 23:59)")
            return
        
        batch_size = self.accounts_per_batch_entry.get().strip()
        if not batch_size.isdigit() or int(batch_size) < 1:
            messagebox.showerror("Invalid Number", "Enter a positive number")
            return
        
        task_name = "SilverBloodAutoClaim"
        exe_path = f"{MAIN_PATH}daily_claiming.exe"
        
        if not self.auto_claim_enabled:
            self._enable_task(task_name, exe_path, batch_size, time_str)
        else:
            self._disable_task(task_name)
    
    def _enable_task(self, task_name, exe_path, batch_size, time_str):
        """Enable task"""
        command = (
            f'schtasks /Create /F /SC DAILY /TN {task_name} '
            f'/TR "{exe_path} {batch_size}" /ST {time_str}'
        )
        
        disable_conditions = (
            f'powershell -Command "'
            f'$task = Get-ScheduledTask -TaskName \'{task_name}\'; '
            f'$task.Settings.DisallowStartIfOnBatteries = $false; '
            f'$task.Settings.StopIfGoingOnBatteries = $false; '
            f'Set-ScheduledTask -TaskName \'{task_name}\' -Settings $task.Settings"'
        )
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        subprocess.run(disable_conditions, shell=True)
        
        if result.returncode == 0:
            self.log_callback(f"✅ Scheduled at {time_str}")
            self.btn_toggle_auto.config(
                text="🔴 Disable Daily Auto-Claim",
                bootstyle="danger"
            )
            self.status_label.config(
                text="🟢 Auto-Claim: Enabled",
                bootstyle="success"
            )
            self.schedule_info.config(
                text=f"Scheduled daily at {time_str}"
            )
            self.auto_claim_enabled = True
            messagebox.showinfo("Success", f"Auto-claim scheduled at {time_str}")
        else:
            self.log_callback(f"❌ Failed: {result.stderr}")
            messagebox.showerror("Error", f"Failed to create task:\n{result.stderr}")
    
    def _disable_task(self, task_name):
        """Disable task"""
        if not messagebox.askyesno("Confirm", "Disable daily auto-claim?"):
            return
        
        command = f'schtasks /Delete /F /TN {task_name}'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            self.log_callback("🗑️ Auto-claim disabled")
            self.btn_toggle_auto.config(
                text="✅ Enable Daily Auto-Claim",
                bootstyle="success"
            )
            self.status_label.config(
                text="⚪ Auto-Claim: Disabled",
                bootstyle="secondary"
            )
            self.schedule_info.config(
                text="No schedule configured"
            )
            self.auto_claim_enabled = False
            messagebox.showinfo("Success", "Auto-claim disabled")
        else:
            self.log_callback(f"❌ Failed: {result.stderr}")
            messagebox.showerror("Error", f"Failed to remove task:\n{result.stderr}")
    
    def get_frame(self):
        """Return frame"""
        return self.frame