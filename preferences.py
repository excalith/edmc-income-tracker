"""
EDMC Income Tracker Plugin - Preferences and configuration management
"""

import tkinter as tk
from config import config
import myNotebook as nb
from ttkHyperlinkLabel import HyperlinkLabel
from utils import (
    CFG_TRACK_TRADING, CFG_TRACK_COMBAT, CFG_TRACK_EXPLORATION, CFG_TRACK_MISSIONS, CFG_TRACK_MAINTENANCE,
    CFG_RESET_ON_CLOSE, get_config_bool, log_debug, log_warning
)

class PreferencesManager:
    """Manages plugin preferences and settings"""

    def __init__(self):
        # Cached tracking settings (updated only when preferences change)
        self.cached_track_trading = True
        self.cached_track_combat = True
        self.cached_track_exploration = True
        self.cached_track_missions = True
        self.cached_track_maintenance = True

        # Reset on close setting
        self.cached_reset_on_close = True

        # UI variables
        self.track_trading = None
        self.track_combat = None
        self.track_exploration = None
        self.track_missions = None
        self.track_maintenance = None
        self.reset_on_close = None

    def load_settings(self):
        """Load settings from config"""
        self.cached_track_trading = get_config_bool(config, CFG_TRACK_TRADING)
        self.cached_track_combat = get_config_bool(config, CFG_TRACK_COMBAT)
        self.cached_track_exploration = get_config_bool(config, CFG_TRACK_EXPLORATION)
        self.cached_track_missions = get_config_bool(config, CFG_TRACK_MISSIONS)
        self.cached_track_maintenance = get_config_bool(config, CFG_TRACK_MAINTENANCE)

        self.cached_reset_on_close = get_config_bool(config, CFG_RESET_ON_CLOSE)

    def create_preferences_ui(self, parent):
        """Create the preferences UI"""
        # Use nb.Frame instead of tk.Frame for EDMC preferences
        frame = nb.Frame(parent)
        frame.columnconfigure(1, weight=1)  # Make second column expandable

        # Title
        HyperlinkLabel(frame, text="EDMC Income Tracker",
                      background=nb.Label().cget('background'),
                      url="https://github.com/excalith/edmc-income-tracker",
                      underline=True).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # Left column - Track options
        nb.Label(frame, text="Track Income From:",
                background=nb.Label().cget('background')).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))

        # Trading tracking
        self.track_trading = tk.BooleanVar(value=self.cached_track_trading)
        tk.Checkbutton(frame,
                      text="Trading (Market Buy/Sell, Trade Data)",
                      variable=self.track_trading,
                      background=nb.Label().cget('background')).grid(row=2, column=0, sticky=tk.W)

        # Combat tracking
        self.track_combat = tk.BooleanVar(value=self.cached_track_combat)
        tk.Checkbutton(frame,
                      text="Combat (Bounties, Vouchers)",
                      variable=self.track_combat,
                      background=nb.Label().cget('background')).grid(row=3, column=0, sticky=tk.W)

        # Exploration tracking
        self.track_exploration = tk.BooleanVar(value=self.cached_track_exploration)
        tk.Checkbutton(frame,
                      text="Exploration (Sell Exploration Data)",
                      variable=self.track_exploration,
                      background=nb.Label().cget('background')).grid(row=4, column=0, sticky=tk.W)

        # Missions tracking
        self.track_missions = tk.BooleanVar(value=self.cached_track_missions)
        tk.Checkbutton(frame,
                      text="Missions (Rewards, Community Goals)",
                      variable=self.track_missions,
                      background=nb.Label().cget('background')).grid(row=5, column=0, sticky=tk.W)

        # Maintenance tracking
        self.track_maintenance = tk.BooleanVar(value=self.cached_track_maintenance)
        tk.Checkbutton(frame,
                      text="Maintenance (Fuel, Repairs, Ammo, etc.)",
                      variable=self.track_maintenance,
                      background=nb.Label().cget('background')).grid(row=6, column=0, sticky=tk.W)

        # Divider
        from tkinter import ttk
        separator = ttk.Separator(frame, orient='horizontal')
        separator.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Reset data on close
        self.reset_on_close = tk.BooleanVar(value=self.cached_reset_on_close)
        tk.Checkbutton(frame,
                      text="Reset data on close",
                      variable=self.reset_on_close,
                      background=nb.Label().cget('background')).grid(row=7, column=0, sticky=tk.W, pady=(0, 10))

        return frame

    def save_settings(self):
        """Save settings to config"""
        # Save track settings
        config.set(CFG_TRACK_TRADING, self.track_trading.get())
        config.set(CFG_TRACK_COMBAT, self.track_combat.get())
        config.set(CFG_TRACK_EXPLORATION, self.track_exploration.get())
        config.set(CFG_TRACK_MISSIONS, self.track_missions.get())
        config.set(CFG_TRACK_MAINTENANCE, self.track_maintenance.get())
        config.set(CFG_RESET_ON_CLOSE, self.reset_on_close.get())

        # Update cached settings
        self.cached_track_trading = self.track_trading.get()
        self.cached_track_combat = self.track_combat.get()
        self.cached_track_exploration = self.track_exploration.get()
        self.cached_track_missions = self.track_missions.get()
        self.cached_track_maintenance = self.track_maintenance.get()
        self.cached_reset_on_close = self.reset_on_close.get()

        log_debug("Income Tracker Plugin preferences saved")
