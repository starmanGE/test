#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Screenshot Monitor Pro - Modern GUI Monitoring Tool
Optimized for performance, simplicity and modern design
"""

import os
import time
import json
import threading
from datetime import datetime
from pathlib import Path

# Try to import GUI libraries, fallback to mock for headless environments
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("GUI libraries not available - running in headless mode")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pyautogui
    SCREENSHOT_AVAILABLE = True
except ImportError:
    SCREENSHOT_AVAILABLE = False


class ScreenshotConfig:
    """Configuration management for screenshot settings"""
    
    def __init__(self):
        self.config_file = Path(__file__).parent / "monitor_config.json"
        self.default_config = {
            'save_path': str(Path.home() / "Screenshots"),
            'interval': 60,
            'screenshot_count': 0,
            'quality': 'high',
            'format': 'png'
        }
        self.config = self.load()
    
    def load(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                return {**self.default_config, **loaded}
            except (json.JSONDecodeError, IOError):
                pass
        return self.default_config.copy()
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError:
            return False
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value


class ScreenshotCapture:
    """Optimized screenshot capture engine"""
    
    def __init__(self, config):
        self.config = config
        self.setup_save_directory()
    
    def setup_save_directory(self):
        """Ensure save directory exists"""
        save_path = Path(self.config.get('save_path'))
        save_path.mkdir(parents=True, exist_ok=True)
    
    def capture(self):
        """Capture screenshot with optimized performance"""
        if not SCREENSHOT_AVAILABLE:
            print("Screenshot functionality not available - simulating capture")
            return self._simulate_capture()
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = Path(self.config.get('save_path')) / filename
            
            # Optimized screenshot capture
            screenshot = pyautogui.screenshot()
            
            # Optimize image if PIL is available
            if PIL_AVAILABLE and self.config.get('quality') == 'optimized':
                screenshot = screenshot.resize(
                    (screenshot.width // 2, screenshot.height // 2),
                    Image.Resampling.LANCZOS
                )
            
            screenshot.save(str(filepath), optimize=True)
            
            # Update count efficiently
            self.config.set('screenshot_count', self.config.get('screenshot_count', 0) + 1)
            
            return {'success': True, 'filename': filename, 'filepath': str(filepath)}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _simulate_capture(self):
        """Simulate screenshot capture for testing"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = Path(self.config.get('save_path')) / filename
        
        # Create dummy file to simulate capture
        try:
            filepath.touch()
            self.config.set('screenshot_count', self.config.get('screenshot_count', 0) + 1)
            return {'success': True, 'filename': filename, 'filepath': str(filepath)}
        except Exception as e:
            return {'success': False, 'error': str(e)}


class MonitorCore:
    """Core monitoring logic with optimized threading"""
    
    def __init__(self, config, capture_engine):
        self.config = config
        self.capture_engine = capture_engine
        self.is_monitoring = False
        self.monitor_thread = None
        self._stop_event = threading.Event()
    
    def start(self):
        """Start monitoring with efficient threading"""
        if self.is_monitoring:
            return False
        
        self.is_monitoring = True
        self._stop_event.clear()
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        return True
    
    def stop(self):
        """Stop monitoring gracefully"""
        if not self.is_monitoring:
            return False
        
        self.is_monitoring = False
        self._stop_event.set()
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        return True
    
    def _monitor_loop(self):
        """Optimized monitoring loop"""
        interval = self.config.get('interval', 60)
        
        while self.is_monitoring and not self._stop_event.is_set():
            result = self.capture_engine.capture()
            
            if result['success']:
                print(f"✓ Captured: {result['filename']}")
            else:
                print(f"✗ Capture failed: {result['error']}")
            
            # Efficient wait with early exit capability
            if self._stop_event.wait(timeout=interval):
                break
    
    def capture_now(self):
        """Immediate screenshot capture"""
        return self.capture_engine.capture()


class ModernGUI:
    """Modern, optimized GUI interface"""
    
    def __init__(self, monitor_core, config):
        if not GUI_AVAILABLE:
            raise RuntimeError("GUI not available in this environment")
        
        self.monitor = monitor_core
        self.config = config
        self.root = None
        self.widgets = {}
        
    def create_interface(self):
        """Create modern, efficient GUI"""
        self.root = tk.Tk()
        self.root.title("📸 Screenshot Monitor Pro")
        self.root.geometry("700x500")
        self.root.configure(bg='#f8f9fa')
        
        # Modern styling
        self._apply_modern_styles()
        
        # Create layout
        self._create_header()
        self._create_settings_panel()
        self._create_control_panel()
        self._create_status_panel()
        
        # Configure responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
    
    def _apply_modern_styles(self):
        """Apply modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button styles with modern colors
        style.configure('Primary.TButton', background='#007bff', foreground='white', 
                       borderwidth=0, padding=(15, 8))
        style.configure('Success.TButton', background='#28a745', foreground='white', 
                       borderwidth=0, padding=(15, 8))
        style.configure('Danger.TButton', background='#dc3545', foreground='white', 
                       borderwidth=0, padding=(15, 8))
        
        # Frame styles
        style.configure('Card.TFrame', background='white', relief='flat', borderwidth=1)
    
    def _create_header(self):
        """Create header section"""
        header = ttk.Frame(self.root, style='Card.TFrame', padding="20")
        header.grid(row=0, column=0, sticky='ew', padx=20, pady=(20, 10))
        
        ttk.Label(header, text="Screenshot Monitor Pro", 
                 font=('Segoe UI', 20, 'bold')).pack(anchor='w')
        ttk.Label(header, text="Automated screenshot capture with modern interface", 
                 font=('Segoe UI', 10), foreground='#6c757d').pack(anchor='w')
    
    def _create_settings_panel(self):
        """Create settings panel"""
        settings = ttk.LabelFrame(self.root, text="⚙️ Configuration", padding="15")
        settings.grid(row=1, column=0, sticky='ew', padx=20, pady=5)
        settings.columnconfigure(1, weight=1)
        
        # Path setting
        ttk.Label(settings, text="Save Path:").grid(row=0, column=0, sticky='w', pady=5)
        
        path_frame = ttk.Frame(settings)
        path_frame.grid(row=0, column=1, sticky='ew', padx=(10, 0))
        path_frame.columnconfigure(0, weight=1)
        
        self.widgets['path_var'] = tk.StringVar(value=self.config.get('save_path'))
        ttk.Entry(path_frame, textvariable=self.widgets['path_var'], 
                 state='readonly').grid(row=0, column=0, sticky='ew', padx=(0, 10))
        ttk.Button(path_frame, text="Browse", 
                  command=self._browse_folder).grid(row=0, column=1)
        
        # Interval setting
        ttk.Label(settings, text="Interval (sec):").grid(row=1, column=0, sticky='w', pady=5)
        self.widgets['interval_var'] = tk.IntVar(value=self.config.get('interval'))
        ttk.Spinbox(settings, from_=1, to=3600, textvariable=self.widgets['interval_var'],
                   width=10).grid(row=1, column=1, sticky='w', padx=(10, 0), pady=5)
    
    def _create_control_panel(self):
        """Create control panel"""
        controls = ttk.Frame(self.root, padding="15")
        controls.grid(row=2, column=0, pady=10)
        
        self.widgets['start_btn'] = ttk.Button(controls, text="▶️ Start", 
                                              style='Success.TButton', command=self._start_monitoring)
        self.widgets['start_btn'].grid(row=0, column=0, padx=5)
        
        self.widgets['stop_btn'] = ttk.Button(controls, text="⏹️ Stop", 
                                             style='Danger.TButton', command=self._stop_monitoring, 
                                             state='disabled')
        self.widgets['stop_btn'].grid(row=0, column=1, padx=5)
        
        ttk.Button(controls, text="📷 Capture", style='Primary.TButton', 
                  command=self._capture_now).grid(row=0, column=2, padx=5)
    
    def _create_status_panel(self):
        """Create status panel"""
        status = ttk.LabelFrame(self.root, text="📊 Status", padding="15")
        status.grid(row=3, column=0, sticky='ew', padx=20, pady=(5, 20))
        status.columnconfigure(1, weight=1)
        
        ttk.Label(status, text="State:").grid(row=0, column=0, sticky='w')
        self.widgets['status_label'] = ttk.Label(status, text="Ready", foreground='#28a745')
        self.widgets['status_label'].grid(row=0, column=1, sticky='w', padx=(10, 0))
        
        ttk.Label(status, text="Count:").grid(row=1, column=0, sticky='w')
        self.widgets['count_label'] = ttk.Label(status, text="0")
        self.widgets['count_label'].grid(row=1, column=1, sticky='w', padx=(10, 0))
    
    def _browse_folder(self):
        """Browse for save folder"""
        folder = filedialog.askdirectory(initialdir=self.config.get('save_path'))
        if folder:
            self.config.set('save_path', folder)
            self.widgets['path_var'].set(folder)
    
    def _start_monitoring(self):
        """Start monitoring"""
        self.config.set('interval', self.widgets['interval_var'].get())
        if self.monitor.start():
            self.widgets['start_btn'].config(state='disabled')
            self.widgets['stop_btn'].config(state='normal')
            self.widgets['status_label'].config(text="Monitoring", foreground='#007bff')
    
    def _stop_monitoring(self):
        """Stop monitoring"""
        if self.monitor.stop():
            self.widgets['start_btn'].config(state='normal')
            self.widgets['stop_btn'].config(state='disabled')
            self.widgets['status_label'].config(text="Ready", foreground='#28a745')
    
    def _capture_now(self):
        """Capture screenshot now"""
        result = self.monitor.capture_now()
        if result['success']:
            self._update_count()
            messagebox.showinfo("Success", f"Captured: {result['filename']}")
        else:
            messagebox.showerror("Error", f"Capture failed: {result['error']}")
    
    def _update_count(self):
        """Update screenshot count display"""
        count = self.config.get('screenshot_count', 0)
        self.widgets['count_label'].config(text=str(count))
    
    def run(self):
        """Run the GUI application"""
        if not self.root:
            self.create_interface()
        
        self._update_count()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.mainloop()
    
    def _on_closing(self):
        """Handle application closing"""
        self.monitor.stop()
        self.config.save()
        self.root.destroy()


class ScreenshotMonitorApp:
    """Main application class with optimized architecture"""
    
    def __init__(self):
        self.config = ScreenshotConfig()
        self.capture_engine = ScreenshotCapture(self.config)
        self.monitor_core = MonitorCore(self.config, self.capture_engine)
        self.gui = None
    
    def run_gui(self):
        """Run with GUI interface"""
        if not GUI_AVAILABLE:
            print("GUI not available - use run_cli() instead")
            return False
        
        self.gui = ModernGUI(self.monitor_core, self.config)
        self.gui.run()
        return True
    
    def run_cli(self):
        """Run with command line interface"""
        print("Screenshot Monitor Pro - CLI Mode")
        print("Commands: start, stop, capture, status, quit")
        
        while True:
            try:
                cmd = input("> ").strip().lower()
                
                if cmd == 'start':
                    if self.monitor_core.start():
                        print("✓ Monitoring started")
                    else:
                        print("✗ Already monitoring")
                
                elif cmd == 'stop':
                    if self.monitor_core.stop():
                        print("✓ Monitoring stopped")
                    else:
                        print("✗ Not monitoring")
                
                elif cmd == 'capture':
                    result = self.monitor_core.capture_now()
                    if result['success']:
                        print(f"✓ Captured: {result['filename']}")
                    else:
                        print(f"✗ Failed: {result['error']}")
                
                elif cmd == 'status':
                    state = "Active" if self.monitor_core.is_monitoring else "Stopped"
                    count = self.config.get('screenshot_count', 0)
                    print(f"Status: {state}, Screenshots: {count}")
                
                elif cmd in ['quit', 'exit']:
                    break
                
                else:
                    print("Unknown command")
                    
            except KeyboardInterrupt:
                break
        
        self.monitor_core.stop()
        self.config.save()
        print("Goodbye!")


def main():
    """Optimized main entry point"""
    app = ScreenshotMonitorApp()
    
    # Try GUI first, fallback to CLI
    if not app.run_gui():
        app.run_cli()


if __name__ == "__main__":
    main()