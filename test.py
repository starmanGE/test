#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Screenshot Monitoring Tool
A modern GUI application for automated screenshot capture and monitoring
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import os
from datetime import datetime
import json
from PIL import Image, ImageTk
import pyautogui
import schedule

class ScreenshotMonitor:
    """Modern Screenshot Monitoring Application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screenshot Monitor Pro")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Application state
        self.is_monitoring = False
        self.monitor_thread = None
        self.save_path = os.path.expanduser("~/Screenshots")
        self.interval = 60  # seconds
        self.screenshot_count = 0
        
        # Create save directory if it doesn't exist
        os.makedirs(self.save_path, exist_ok=True)
        
        # Load settings
        self.load_settings()
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.update_status()
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background='#007bff',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Primary.TButton',
                 background=[('active', '#0056b3')])
        
        style.configure('Success.TButton',
                       background='#28a745',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Success.TButton',
                 background=[('active', '#1e7e34')])
        
        style.configure('Danger.TButton',
                       background='#dc3545',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Danger.TButton',
                 background=[('active', '#c82333')])
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="📸 Screenshot Monitor Pro", 
                               font=('Segoe UI', 24, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(header_frame, text="Automated screenshot capture and monitoring",
                                  font=('Segoe UI', 12), foreground='#6c757d')
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Settings", padding="15")
        settings_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        settings_frame.columnconfigure(1, weight=1)
        
        # Save path setting
        ttk.Label(settings_frame, text="Save Location:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        path_frame = ttk.Frame(settings_frame)
        path_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        path_frame.columnconfigure(0, weight=1)
        
        self.path_var = tk.StringVar(value=self.save_path)
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, state='readonly')
        path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_folder)
        browse_btn.grid(row=0, column=1)
        
        # Interval setting
        ttk.Label(settings_frame, text="Interval (seconds):").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.interval_var = tk.IntVar(value=self.interval)
        interval_spin = ttk.Spinbox(settings_frame, from_=1, to=3600, textvariable=self.interval_var,
                                   width=10, command=self.update_interval)
        interval_spin.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Control Frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        self.start_btn = ttk.Button(control_frame, text="▶️ Start Monitoring", 
                                   style='Success.TButton', command=self.start_monitoring)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="⏹️ Stop Monitoring", 
                                  style='Danger.TButton', command=self.stop_monitoring, state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        capture_btn = ttk.Button(control_frame, text="📷 Capture Now", 
                                style='Primary.TButton', command=self.capture_now)
        capture_btn.grid(row=0, column=2, padx=5)
        
        # Status Frame
        status_frame = ttk.LabelFrame(main_frame, text="📊 Status", padding="15")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        status_frame.columnconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.status_label = ttk.Label(status_frame, text="Ready", foreground='#28a745', font=('Segoe UI', 10, 'bold'))
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(status_frame, text="Screenshots Taken:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.count_label = ttk.Label(status_frame, text="0", font=('Segoe UI', 10, 'bold'))
        self.count_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(status_frame, text="Next Capture:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.next_label = ttk.Label(status_frame, text="Manual", font=('Segoe UI', 10))
        self.next_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        open_folder_btn = ttk.Button(footer_frame, text="📁 Open Screenshots Folder", 
                                    command=self.open_screenshots_folder)
        open_folder_btn.grid(row=0, column=0, padx=5)
        
        settings_btn = ttk.Button(footer_frame, text="💾 Save Settings", 
                                 command=self.save_settings)
        settings_btn.grid(row=0, column=1, padx=5)
    
    def browse_folder(self):
        """Browse for screenshot save location"""
        folder = filedialog.askdirectory(initialdir=self.save_path)
        if folder:
            self.save_path = folder
            self.path_var.set(folder)
    
    def update_interval(self):
        """Update monitoring interval"""
        self.interval = self.interval_var.get()
    
    def start_monitoring(self):
        """Start automatic screenshot monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.progress.start(10)
            
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
            
            self.update_status()
    
    def stop_monitoring(self):
        """Stop automatic screenshot monitoring"""
        self.is_monitoring = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.progress.stop()
        self.update_status()
    
    def monitor_loop(self):
        """Main monitoring loop"""
        next_capture = time.time() + self.interval
        
        while self.is_monitoring:
            current_time = time.time()
            
            if current_time >= next_capture:
                self.capture_screenshot()
                next_capture = current_time + self.interval
            
            # Update next capture time display
            remaining = max(0, int(next_capture - current_time))
            self.root.after(0, lambda: self.next_label.config(
                text=f"In {remaining} seconds"))
            
            time.sleep(1)
    
    def capture_now(self):
        """Capture screenshot immediately"""
        self.capture_screenshot()
    
    def capture_screenshot(self):
        """Capture and save screenshot"""
        try:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.save_path, filename)
            
            # Capture screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            # Update counter
            self.screenshot_count += 1
            self.root.after(0, lambda: self.count_label.config(text=str(self.screenshot_count)))
            
            # Show success message briefly
            self.root.after(0, lambda: self.status_label.config(
                text=f"Captured: {filename}", foreground='#28a745'))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", f"Failed to capture screenshot: {str(e)}"))
    
    def update_status(self):
        """Update status display"""
        if self.is_monitoring:
            self.status_label.config(text="Monitoring Active", foreground='#007bff')
        else:
            self.status_label.config(text="Ready", foreground='#28a745')
            self.next_label.config(text="Manual")
    
    def open_screenshots_folder(self):
        """Open screenshots folder in file explorer"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.save_path)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{self.save_path}"' if os.uname().sysname == 'Darwin' 
                         else f'xdg-open "{self.save_path}"')
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {str(e)}")
    
    def load_settings(self):
        """Load settings from config file"""
        try:
            settings_file = os.path.join(os.path.dirname(__file__), 'monitor_settings.json')
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    self.save_path = settings.get('save_path', self.save_path)
                    self.interval = settings.get('interval', self.interval)
                    self.screenshot_count = settings.get('screenshot_count', 0)
        except Exception:
            pass  # Use defaults if loading fails
    
    def save_settings(self):
        """Save current settings to config file"""
        try:
            settings = {
                'save_path': self.save_path,
                'interval': self.interval,
                'screenshot_count': self.screenshot_count
            }
            settings_file = os.path.join(os.path.dirname(__file__), 'monitor_settings.json')
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save settings: {str(e)}")
    
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_monitoring:
            self.stop_monitoring()
        self.save_settings()
        self.root.destroy()

def main():
    """Main entry point"""
    try:
        app = ScreenshotMonitor()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
    except Exception as e:
        print(f"Application error: {e}")

if __name__ == "__main__":
    main()