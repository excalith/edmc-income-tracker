"""
EDMC Income Tracker Plugin - Utility functions and constants
"""

import logging
import os
import sys
import time
import tkinter as tk

# Debug settings
DEBUG_MODE = True


# Plugin information
plugin_name = os.path.basename(os.path.dirname(__file__))

# Set up logging
logger = logging.getLogger(f'{plugin_name}.{__name__}')

# Configuration keys
CFG_EARNINGS = "EDMCIncome_earnings"
CFG_TRACK_TRADING = "EDMCIncome_track_trading"
CFG_TRACK_COMBAT = "EDMCIncome_track_combat"
CFG_TRACK_EXPLORATION = "EDMCIncome_track_exploration"
CFG_TRACK_MISSIONS = "EDMCIncome_track_missions"

CFG_RESET_ON_CLOSE = "EDMCIncome_reset_on_close"

# Module globals
this = sys.modules[__name__]

class Transaction:
    """Represents a transaction"""
    def __init__(self, earnings: float, category: str = "unknown"):
        self.earnings = earnings
        self.category = category
        self.time = time.time()

def get_config_bool(config, key: str, default: bool = True) -> bool:
    """Get boolean config value with fallback"""
    if config.get_int(key) is not None:
        return bool(config.getint(key))
    return default

def log_event(event_name: str, earnings: float, category: str) -> None:
    """Log a transaction event"""
    logger.debug(f"Income Tracker: Transaction recorded: {earnings:,.0f} Cr ({category})")

def log_debug(message: str) -> None:
    """Log debug message"""
    logger.debug(message)

def log_warning(message: str) -> None:
    """Log warning message"""
    logger.warning(message)

class Tooltip:
    """Tooltip widget using tkinter's built-in functionality"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind('<Enter>', self.show_tooltip)
        self.widget.bind('<Leave>', self.hide_tooltip)
        self.widget.bind('<Button-1>', self.hide_tooltip)  # Hide on click too

    def show_tooltip(self, event=None):
        try:
            # Get widget position
            x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
            y = self.widget.winfo_rooty() + 5

            # Create tooltip window
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")

            # Make sure tooltip is on top
            self.tooltip.attributes('-topmost', True)

            # Create tooltip label
            label = tk.Label(self.tooltip, text=self.text,
                            justify=tk.LEFT, background="#ffffe0",
                            relief=tk.SOLID, borderwidth=1,
                            font=("Tahoma", "8", "normal"),
                            wraplength=200)  # Wrap long text
            label.pack(padx=2, pady=2)

            # Schedule auto-hide after 3 seconds
            self.widget.after(3000, self.hide_tooltip)
        except Exception as e:
            # If tooltip fails, just log it and continue
            log_debug(f"Tooltip failed: {e}")

    def hide_tooltip(self, event=None):
        if self.tooltip:
            try:
                self.tooltip.destroy()
            except:
                pass
            self.tooltip = None
