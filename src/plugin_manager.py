"""
EDMC Income Tracker Plugin - Plugin Manager for component lifecycle
"""

import tkinter as tk
from src.utils import log_debug, log_warning, log_critical
from src.preferences import PreferencesManager
from src.ui import IncomeTrackerUI
from src.income_tracker import EDMCIncome
from src.journal_processor import JournalProcessor


class PluginManager:
    """Manages the lifecycle of all plugin components"""

    def __init__(self):
        self.preferences_manager = None
        self.income_tracker = None
        self.ui_manager = None
        self.journal_processor = None

    def initialize(self) -> str:
        """
        Initialize all plugin components.

        Returns:
            Plugin name to be displayed in the EDMC status bar
        """
        log_debug("EDMC Income Tracker Plugin starting...")
        log_debug("Plugin functions available: plugin_prefs, prefs_changed")

        # Log version checker initialization
        try:
            from src.constants import PLUGIN_VERSION
            log_debug(f"[VERSIONCODE] Plugin Manager: Initializing with version {PLUGIN_VERSION}")
        except ImportError:
            log_critical("Failed to import constants or utils")
            pass

        # Initialize components
        self.preferences_manager = PreferencesManager()
        self.preferences_manager.load_settings()

        # Initialize UI manager (will be properly set up in plugin_app)
        self.ui_manager = None

        # Initialize the income tracker
        self.income_tracker = EDMCIncome(self.ui_manager)
        self.income_tracker.load()

        # Initialize journal processor
        self.journal_processor = JournalProcessor(self.income_tracker, self.preferences_manager)

        # Load state
        self.income_tracker.load_state(self.preferences_manager.cached_reset_on_close)

        from src.constants import PLUGIN_NAME
        return PLUGIN_NAME

    def cleanup(self) -> None:
        """
        Clean up plugin components on shutdown.
        """
        log_debug("Income Tracker Plugin stopping...")

        # Clear income data on app close
        if self.income_tracker:
            if self.preferences_manager and self.preferences_manager.cached_reset_on_close:
                # Reset clears both current session and previous sessions
                self.income_tracker.reset()
                log_debug("Income Tracker data cleared on app close (all sessions)")
            else:
                self.income_tracker.save_state()
                log_debug("Income Tracker data NOT cleared on app close due to preference")

    def setup_ui(self, parent: tk.Frame) -> tk.Frame:
        """
        Set up the plugin's main UI.

        Args:
            parent: The parent frame to attach our UI to

        Returns:
            The frame containing our plugin's UI
        """
        # Initialize UI manager
        self.ui_manager = IncomeTrackerUI(self.income_tracker, self.preferences_manager, self.journal_processor)

        # Update income tracker with UI reference
        self.income_tracker.ui = self.ui_manager

        # Add journal_processor to income_tracker so UI can access it for debug
        self.income_tracker.journal_processor = self.journal_processor

        # Create and return the UI
        return self.ui_manager.create_main_ui(parent)

    def create_preferences_ui(self, parent) -> tk.Frame:
        """
        Create the plugin's preferences/settings panel.

        Args:
            parent: The parent frame for preferences UI

        Returns:
            The preferences frame, or None if not available
        """
        if self.preferences_manager:
            return self.preferences_manager.create_preferences_ui(parent)
        return None

    def save_preferences(self) -> None:
        """
        Save preferences and update the display.
        """
        log_debug("prefs_changed() called!")

        if self.preferences_manager:
            self.preferences_manager.save_settings()

            # Update the display if income tracker exists
            if self.income_tracker:
                log_debug("Updating display after preferences change")
                self.income_tracker.update_window()

                # Refresh UI visibility if UI manager exists
                if self.ui_manager:
                    self.ui_manager.refresh_ui()
            else:
                log_warning("Income tracker not found, cannot update display")

    def process_journal_entry(self, cmdr: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> str:
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
        if self.journal_processor:
            return self.journal_processor.process_journal_entry(cmdr, is_beta, system, station, entry, state)
        return None

    def process_dashboard_entry(self, cmdr: str, is_beta: bool, entry: dict) -> None:
        """
        Process a status.json entry (dashboard data).

        Args:
            cmdr: The current commander name
            is_beta: Whether running in beta mode
            entry: The status.json entry as a dictionary
        """
        if self.journal_processor:
            self.journal_processor.process_dashboard_entry(cmdr, is_beta, entry)
