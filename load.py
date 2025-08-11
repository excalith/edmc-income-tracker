"""
EDMC Income Tracker Plugin - Track your income and earnings in Elite Dangerous
"""

import tkinter as tk
import sys
from config import config

# Import our modular components
from src.utils import log_debug
from src.plugin_manager import PluginManager

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

# Global plugin manager instance
this.plugin_manager = None

def plugin_start3(plugin_dir: str) -> str:
    """
    Load the plugin. This is called once when the plugin is loaded.

    Args:
        plugin_dir: The directory containing this plugin

    Returns:
        Plugin name to be displayed in the EDMC status bar
    """
    # Initialize plugin manager
    this.plugin_manager = PluginManager()
    return this.plugin_manager.initialize()

def plugin_stop() -> None:
    """
    Stop the plugin. This is called when EDMC is shutting down.
    """
    if this.plugin_manager:
        this.plugin_manager.cleanup()

def plugin_app(parent: tk.Frame) -> tk.Frame:
    """
    Create the plugin's main UI frame.

    Args:
        parent: The parent frame to attach our UI to

    Returns:
        The frame containing our plugin's UI
    """
    if this.plugin_manager:
        return this.plugin_manager.setup_ui(parent)
    return None

def plugin_prefs(parent, cmdr, is_beta):
    """
    Create the plugin's preferences/settings panel.
    """
    if this.plugin_manager:
        return this.plugin_manager.create_preferences_ui(parent)
    return None

def prefs_changed(cmdr, is_beta):
    """
    Called when the user clicks OK on the preferences dialog.
    """
    if this.plugin_manager:
        this.plugin_manager.save_preferences()

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
    if this.plugin_manager:
        return this.plugin_manager.process_journal_entry(cmdr, is_beta, system, station, entry, state)
    return None

def dashboard_entry(cmdr: str, is_beta: bool, entry: dict) -> None:
    """
    Process a status.json entry (dashboard data).

    Args:
        cmdr: The current commander name
        is_beta: Whether running in beta mode
        entry: The status.json entry as a dictionary
    """
    if this.plugin_manager:
        this.plugin_manager.process_dashboard_entry(cmdr, is_beta, entry)
