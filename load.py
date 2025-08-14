"""
EDMC Income Tracker Plugin - Track your income and earnings in Elite Dangerous
"""

import tkinter as tk
import sys
from config import config # type: ignore
from src.utils import log_info, log_error, log_warning, log_debug, log_critical

# Import our modular components
from src.plugin_manager import PluginManager

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
    try:
        from src.constants import PLUGIN_NAME, PLUGIN_VERSION
        from src.utils import log_debug
        log_debug(f"[VERSIONCODE] Plugin starting - {PLUGIN_NAME} v{PLUGIN_VERSION}")
    except ImportError as e:
        log_critical(f"Failed to import constants or utils: {e}")

    # Initialize plugin manager
    this.plugin_manager = PluginManager()

    try:
        result = this.plugin_manager.initialize()
        log_info(f"Plugin initialized successfully: {result}")
        return result
    except Exception as e:
        log_error(f"Plugin initialization failed: {e}")
        return "Initialization failed"

def plugin_stop() -> None:
    """
    Stop the plugin. This is called when EDMC is shutting down.
    """
    if this.plugin_manager:
        try:
            this.plugin_manager.cleanup()
            log_info("Plugin stopped and cleaned up successfully")
        except Exception as e:
            log_error(f"Error during plugin cleanup: {e}")
    else:
        log_warning("plugin_stop() called but plugin_manager is None")

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
        try:
            ui = this.plugin_manager.create_preferences_ui(parent)
            log_debug("Preferences UI created")
            return ui
        except Exception as e:
            log_error(f"Failed to create preferences UI: {e}")
            return None
    else:
        log_warning("plugin_prefs() called but plugin_manager is None")
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
