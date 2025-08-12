"""
EDMC Income Tracker Plugin - Preferences and configuration management
"""

import tkinter as tk
from tkinter import ttk
from config import config # type: ignore
import myNotebook as nb # type: ignore
from ttkHyperlinkLabel import HyperlinkLabel # type: ignore
from src.constants import (
    CFG_TRACK_TRADING, CFG_TRACK_COMBAT, CFG_TRACK_EXPLORATION, CFG_TRACK_MISSIONS,
    CFG_RESET_ON_CLOSE, CFG_SHOW_TOTAL_CREDITS, GITHUB_REPO_URL, PLUGIN_VERSION, GITHUB_API_URL, PLUGIN_NAME
)
from src.update_checker import check_for_updates
from src.utils import get_config_bool, log_debug, Tooltip


class PreferencesManager:
    """Manages plugin preferences and settings"""

    def _create_checkbox(self, frame, text, variable, tooltip_text=None, columnspan=2):
        """Create a checkbox with consistent styling and optional tooltip"""
        cb = nb.Checkbutton(frame, text=text, variable=variable)
        cb.grid(row=self.current_row, column=0, columnspan=columnspan, sticky=tk.W, pady=(0, 5))

        if tooltip_text:
            Tooltip(cb, tooltip_text)

        # Auto-increment row for next element
        self.current_row += 1

        return cb

    def _create_dropdown(self, frame, text, variable, options, tooltip_text=None):
        """Create a dropdown with consistent styling and optional tooltip"""
        # Create label
        label = nb.Label(frame, text=text)
        label.grid(row=self.current_row, column=0, sticky=tk.W, pady=(0, 5))
        if tooltip_text:
            Tooltip(label, tooltip_text)

        # Create dropdown
        dropdown = nb.OptionMenu(frame, variable, variable.get(), *options)
        dropdown.grid(row=self.current_row, column=1, sticky=tk.W, pady=(0, 5))


        # Auto-increment row for next element
        self.current_row += 1

        return label, dropdown

    def _create_section_header(self, frame, text):
        """Create a section header with consistent styling"""
        header = nb.Label(frame, text=text, font=("TkDefaultFont", 9, "bold"))
        header.grid(row=self.current_row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))

        # Auto-increment row for next element
        self.current_row += 1

        return header

    def _create_divider(self, frame):
        """Create a horizontal divider"""
        separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
        separator.grid(row=self.current_row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Auto-increment row for next element
        self.current_row += 1

        return separator

    def _create_title_section(self, frame, title_text, version, repo_url, update_info=None):
        """Create the title section with version and optional update link"""
        title_frame = nb.Frame(frame)
        title_frame.grid(row=self.current_row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # Main title
        title_label = HyperlinkLabel(title_frame, text=f"EDMC {title_text} v{version}",
                                   url=repo_url,
                                   background=nb.Label().cget('background'),
                                   underline=True)
        title_label.grid(row=0, column=0, sticky=tk.W)

        # Update link (if available)
        if update_info and update_info.get('has_update'):
            log_debug(f"[VERSIONCODE] Preferences UI: Showing update link for v{update_info['latest_version']}")
            update_label = HyperlinkLabel(title_frame,
                                       text=f"(v{update_info['latest_version']} available)",
                                       url=update_info['download_url'],
                                       background=nb.Label().cget('background'),
                                       underline=True)
            update_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
            Tooltip(update_label, f"Click to download version {update_info['latest_version']}")
        else:
            log_debug("[VERSIONCODE] Preferences UI: No update available, not showing update link")

        # Auto-increment row for next element
        self.current_row += 1

        return title_frame

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

        # Show Total Credits setting
        self.cached_show_total_credits = True

        # UI variables
        self.track_trading = None
        self.track_combat = None
        self.track_exploration = None
        self.track_missions = None
        self.reset_on_close = None
        self.view_mode = None
        self.show_total_credits = None

        # UI row tracking
        self.current_row = 0

    def load_settings(self):
        """Load settings from config"""
        # Load settings with True as default (tracking enabled by default)
        self.cached_track_trading = get_config_bool(config, CFG_TRACK_TRADING, default=True)
        self.cached_track_combat = get_config_bool(config, CFG_TRACK_COMBAT, default=True)
        self.cached_track_exploration = get_config_bool(config, CFG_TRACK_EXPLORATION, default=True)
        self.cached_track_missions = get_config_bool(config, CFG_TRACK_MISSIONS, default=True)

        self.cached_reset_on_close = get_config_bool(config, CFG_RESET_ON_CLOSE, default=True)

        self.cached_view_mode = config.get_str("view_mode", default="full")
        self.cached_show_total_credits = get_config_bool(config, CFG_SHOW_TOTAL_CREDITS, default=True)

    def save_settings(self):
        """Save settings to config"""
        # Save track settings
        config.set(CFG_TRACK_TRADING, self.track_trading.get())
        config.set(CFG_TRACK_COMBAT, self.track_combat.get())
        config.set(CFG_TRACK_EXPLORATION, self.track_exploration.get())
        config.set(CFG_TRACK_MISSIONS, self.track_missions.get())
        config.set(CFG_RESET_ON_CLOSE, self.reset_on_close.get())
        config.set(CFG_SHOW_TOTAL_CREDITS, self.show_total_credits.get())

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
        self.cached_show_total_credits = self.show_total_credits.get()
        self.cached_view_mode = internal_view_mode

        log_debug("Income Tracker Plugin preferences saved")

    def create_preferences_ui(self, parent):
        """Create the preferences UI"""
        # Load current settings first
        self.load_settings()

        # nb.Frame for EDMC preferences
        frame = nb.Frame(parent)
        frame.columnconfigure(1, weight=1)

        # Check for updates
        log_debug("[VERSIONCODE] Preferences UI: Starting version check...")
        update_info = check_for_updates(PLUGIN_VERSION, GITHUB_API_URL)
        log_debug(f"[VERSIONCODE] Preferences UI: Version check result: {update_info}")

        #region Title
        # Title
        # Create title section
        self.current_row = 0
        self._create_title_section(frame, PLUGIN_NAME, PLUGIN_VERSION, GITHUB_REPO_URL, update_info)
        #endregion

        #region Plugin Settings
        self._create_section_header(frame, "Settings:")

        # View mode
        view_mode_options = {
            "full": "Full View - All Information",
            "compact": "Compact View - Essential Only"
        }
        display_text = view_mode_options.get(self.cached_view_mode, "Full View - All Information")
        self.view_mode = tk.StringVar(value=display_text)

        self._create_dropdown(
            frame,
            "View Mode:",
            self.view_mode,
            view_mode_options.values(),
            "Full: Shows all information including maintenance and category breakdown\n\nCompact: Shows only essential information (title, reset, hourly, income)"
        )

        # Show Total Credits option
        self.show_total_credits = tk.BooleanVar(value=self.cached_show_total_credits)
        self._create_checkbox(
            frame,
            "Display current credit balance",
            self.show_total_credits,
            "Shows your current credit balance"
        )

        # Reset data on close
        self.reset_on_close = tk.BooleanVar(value=self.cached_reset_on_close)
        self._create_checkbox(
            frame,
            "Reset data on close",
            self.reset_on_close,
            "Enabled: All current session earnings will be reset when EDMC is closed.\n\nDisabled: Earnings persist between sessions.",
            columnspan=2
        )
        #endregion

        self._create_divider(frame)

        #region Tracker Settings
        self._create_section_header(frame, "Track Income From:")

        # Define tracking options with their data
        tracking_options = [
            ("Trading", "track_trading", "Track income from:\nBuying/Selling Commodities\nTrade Data purchases"),
            ("Combat", "track_combat", "Track income from:\nBounty Vouchers and Combat Bonds\nPaying Fines and Bounties"),
            ("Exploration", "track_exploration", "Track income from:\nBuying/Selling Exploration Data, including bonuses for first discoveries"),
            ("Missions", "track_missions", "Track income from:\nMission Rewards and Fail Penalties\nCommunity Goal Rewards")
        ]

        # Create checkboxes
        for text, var_name, tooltip_text in tracking_options:
            # Create the BooleanVar with the cached value
            cached_value = getattr(self, f"cached_{var_name}")
            var = tk.BooleanVar(value=cached_value)
            setattr(self, var_name, var)

            self._create_checkbox(frame, text, var, tooltip_text)
        #endregion

        return frame

