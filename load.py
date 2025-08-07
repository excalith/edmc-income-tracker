"""
EDMC Income Tracker Plugin - Track your income and earnings in Elite Dangerous
"""

import tkinter as tk
import logging
import os
import sys
from config import config

# Import our modular components
from utils import plugin_name, logger, log_debug, log_warning
from preferences import PreferencesManager
from ui import IncomeTrackerUI
from income_tracker import EDMCIncome
from journal_processor import JournalProcessor

# For compatibility with pre-5.0.0
if not hasattr(config, 'get_int'):
    config.get_int = config.getint

if not hasattr(config, 'get_str'):
    config.get_str = config.get

if not hasattr(config, 'get_bool'):
    config.get_bool = lambda key: bool(config.getint(key))

if not hasattr(config, 'get_list'):
    config.get_list = config.get

# Module globals
this = sys.modules[__name__]

# Global instances
this.preferences_manager = None
this.income_tracker = None
this.ui_manager = None
this.journal_processor = None

def plugin_start3(plugin_dir: str) -> str:
    """
    Load the plugin. This is called once when the plugin is loaded.

    Args:
        plugin_dir: The directory containing this plugin

    Returns:
        Plugin name to be displayed in the EDMC status bar
    """
    log_debug("EDMC Income Tracker Plugin starting...")
    log_debug("Plugin functions available: plugin_prefs, prefs_changed")

    # Initialize components
    this.preferences_manager = PreferencesManager()
    this.preferences_manager.load_settings()

    # Initialize UI manager (will be properly set up in plugin_app)
    this.ui_manager = None

    # Initialize the income tracker
    this.income_tracker = EDMCIncome(this.ui_manager)
    this.income_tracker.load()

    # Initialize journal processor
    this.journal_processor = JournalProcessor(this.income_tracker, this.preferences_manager)

    return "IncomeTracker"

def plugin_stop() -> None:
    """
    Stop the plugin. This is called when EDMC is shutting down.
    """
    log_debug("Income Tracker Plugin stopping...")

    # Clear income data on app close
    if this.income_tracker:
        if this.preferences_manager and this.preferences_manager.cached_reset_on_close:
            this.income_tracker.reset()
            log_debug("Income Tracker data cleared on app close")
        else:
            log_debug("Income Tracker data NOT cleared on app close due to preference")

def plugin_app(parent: tk.Frame) -> tk.Frame:
    """
    Create the plugin's main UI frame.

    Args:
        parent: The parent frame to attach our UI to

    Returns:
        The frame containing our plugin's UI
    """
    # Initialize UI manager
    this.ui_manager = IncomeTrackerUI(this.income_tracker, this.preferences_manager)

    # Update income tracker with UI reference
    this.income_tracker.ui = this.ui_manager

    # Create and return the UI
    return this.ui_manager.create_main_ui(parent)

def plugin_prefs(parent, cmdr, is_beta):
    """
    Create the plugin's preferences/settings panel.
    """
    if this.preferences_manager:
        return this.preferences_manager.create_preferences_ui(parent)
    return None

def prefs_changed(cmdr, is_beta):
    """
    Called when the user clicks OK on the preferences dialog.
    """
    log_debug("prefs_changed() called!")

    if this.preferences_manager:
        this.preferences_manager.save_settings()

        # Update the display if income tracker exists
        if this.income_tracker:
            log_debug("Updating display after preferences change")
            this.income_tracker.update_window()
            this.income_tracker.update_widget_visibility()
            this.income_tracker.update_breakdown_visibility()
        else:
            log_warning("Income tracker not found, cannot update display")

def journal_entry(cmdr: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> str:
    """
    Process a journal entry.

    Args:
        cmdr: The current commander name
        is_beta: Whether running in beta mode
        system: Current system name
        station: Current station name
        entry: The journal entry as a dictionary
        state: The current game state

    Returns:
        Status message to display in EDMC, or None
    """
    if this.journal_processor:
        return this.journal_processor.process_journal_entry(cmdr, is_beta, system, station, entry, state)
    return None

def dashboard_entry(cmdr: str, is_beta: bool, entry: dict) -> None:
    """
    Process a status.json entry (dashboard data).

    Args:
        cmdr: The current commander name
        is_beta: Whether running in beta mode
        entry: The status.json entry as a dictionary
    """
    if this.journal_processor:
        this.journal_processor.process_dashboard_entry(cmdr, is_beta, entry)
