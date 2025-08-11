"""
EDMC Income Tracker Plugin - Preferences and configuration management
"""

import tkinter as tk
from tkinter import ttk
from config import config
import myNotebook as nb
from ttkHyperlinkLabel import HyperlinkLabel
from utils import (
    CFG_TRACK_TRADING, CFG_TRACK_COMBAT, CFG_TRACK_EXPLORATION, CFG_TRACK_MISSIONS,
    CFG_RESET_ON_CLOSE, get_config_bool, log_debug, log_warning, Tooltip
)

class PreferencesManager:
    """Manages plugin preferences and settings"""

    def __init__(self):
        # Cached tracking settings (updated only when preferences change)
        self.cached_track_trading = True
        self.cached_track_combat = True
        self.cached_track_exploration = True
        self.cached_track_missions = True

        # Reset on close setting
        self.cached_reset_on_close = True

        # View mode setting
        self.cached_view_mode = "full"

        # UI variables
        self.track_trading = None
        self.track_combat = None
        self.track_exploration = None
        self.track_missions = None
        self.reset_on_close = None
        self.view_mode = None

    def load_settings(self):
        """Load settings from config"""
        # Load settings with True as default (tracking enabled by default)
        self.cached_track_trading = get_config_bool(config, CFG_TRACK_TRADING, default=True)
        self.cached_track_combat = get_config_bool(config, CFG_TRACK_COMBAT, default=True)
        self.cached_track_exploration = get_config_bool(config, CFG_TRACK_EXPLORATION, default=True)
        self.cached_track_missions = get_config_bool(config, CFG_TRACK_MISSIONS, default=True)

        self.cached_reset_on_close = get_config_bool(config, CFG_RESET_ON_CLOSE, default=True)

        self.cached_view_mode = config.get_str("view_mode", default="full")

    def create_preferences_ui(self, parent):
        """Create the preferences UI"""
        # Load current settings first
        self.load_settings()

        # Use nb.Frame instead of tk.Frame for EDMC preferences
        frame = nb.Frame(parent)
        frame.columnconfigure(1, weight=1)  # Make second column expandable

        # Title
        HyperlinkLabel(frame, text="EDMC Income Tracker",
                      url="https://github.com/excalith/edmc-income-tracker",
                      background=nb.Label().cget('background'),
                      underline=True).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        #region Plugin Settings
        nb.Label(frame, text="Settings:", font=("TkDefaultFont", 9, "bold")).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))

        # View mode
        nb.Label(frame, text="View Mode:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        view_mode_options = {
            "full": "Full View - All Information",
            "compact": "Compact View - Essential Only"
        }

        display_text = view_mode_options.get(self.cached_view_mode, "Full View - All Information")
        self.view_mode = tk.StringVar(value=display_text)

        view_dropdown = nb.OptionMenu(
            frame,
            self.view_mode,
            display_text,  # Show display text
            *view_mode_options.values()  # Pass display values to dropdown
        )
        view_dropdown.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
        Tooltip(view_dropdown, "Full: Shows all information including maintenance and category breakdown\nCompact: Shows only essential information (title, reset, hourly, income)")

        # Reset data on close
        self.reset_on_close = tk.BooleanVar(value=self.cached_reset_on_close)
        reset_cb = nb.Checkbutton(frame,
                      text="Reset data on close",
                      variable=self.reset_on_close)
        reset_cb.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        Tooltip(reset_cb, "When enabled, all current session earnings will be reset when EDMC is closed.\nWhen disabled, earnings persist between sessions.")
        #endregion

        # Divider
        separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
        separator.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        #region Tracker Settings
        # Track options header
        nb.Label(frame, text="Track Income From:", font=("TkDefaultFont", 9, "bold")).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))

        # Define tracking options with their data
        tracking_options = [
            ("Trading", "track_trading", "Track income from Buying/Selling Commodities and Trade Data purchases"),
            ("Combat", "track_combat", "Track income from Bounty Vouchers, Combat Bonds, and other combat-related rewards"),
            ("Exploration", "track_exploration", "Track income from selling Exploration Data, including bonuses for first discoveries"),
            ("Missions", "track_missions", "Track income from Mission Rewards, Community Goal Rewards")
        ]

        # Create checkboxes dynamically
        for i, (text, var_name, tooltip_text) in enumerate(tracking_options, start=6):
            # Create the BooleanVar with the cached value
            cached_value = getattr(self, f"cached_{var_name}")
            var = tk.BooleanVar(value=cached_value)
            setattr(self, var_name, var)

            cb = nb.Checkbutton(frame,
                              text=text,
                              variable=var)
            cb.grid(row=i, column=0, columnspan=2, sticky=tk.W)

            # Add tooltip
            Tooltip(cb, tooltip_text)
        #endregion

        return frame

    def save_settings(self):
        """Save settings to config"""
        # Save track settings
        config.set(CFG_TRACK_TRADING, self.track_trading.get())
        config.set(CFG_TRACK_COMBAT, self.track_combat.get())
        config.set(CFG_TRACK_EXPLORATION, self.track_exploration.get())
        config.set(CFG_TRACK_MISSIONS, self.track_missions.get())
        config.set(CFG_RESET_ON_CLOSE, self.reset_on_close.get())
        # Convert display text back to internal key for view mode
        view_mode_options = {
            "Full View - All Information": "full",
            "Compact View - Essential Only": "compact"
        }
        internal_view_mode = view_mode_options.get(self.view_mode.get(), "full")
        config.set("view_mode", internal_view_mode)

        # Update cached settings
        self.cached_track_trading = self.track_trading.get()
        self.cached_track_combat = self.track_combat.get()
        self.cached_track_exploration = self.track_exploration.get()
        self.cached_track_missions = self.track_missions.get()
        self.cached_reset_on_close = self.reset_on_close.get()
        self.cached_view_mode = internal_view_mode

        log_debug("Income Tracker Plugin preferences saved")
