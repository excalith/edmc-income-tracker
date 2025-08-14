"""
EDMC Income Tracker Plugin - Debug testing interface (with real data)
"""

import os
import json
import tkinter as tk
from src.utils import log_debug
from src.constants import JOURNAL_EVENT_CATEGORIES

DEBUG_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class DebugInterface:
    """Debug interface for testing journal events with real example data"""

    def __init__(self, journal_processor, income_tracker):
        self.journal_processor = journal_processor
        self.income_tracker = income_tracker

    def create_debug_frame(self, parent):
        """Create the debug interface frame"""
        log_debug("DEBUG: Creating debug frame")
        frame = tk.Frame(parent)

        # Debug header
        header = tk.Label(
            frame,
            text="---- DEBUG ----",
            font=("Euro Caps", 10, "bold"),
            fg="#ff8000"
        )
        header.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)

        row = 1
        for category, events in JOURNAL_EVENT_CATEGORIES.items():
            if category == "maintenance":
                continue

            log_debug(f"DEBUG: Creating category {category} with {len(events)} events")

            # Category title
            title = tk.Label(
                frame,
                text=category.capitalize(),
                font=("Euro Caps", 9, "bold")
            )
            title.grid(row=row, column=0, sticky=tk.W, pady=(5, 2))

            # Event buttons in second column
            button_frame = tk.Frame(frame)
            button_frame.grid(row=row, column=1, sticky=tk.W, padx=(10, 0))

            for event_name in events.keys():
                log_debug(f"DEBUG: Creating button for {event_name}")
                # Use a function factory to avoid lambda closure issues
                def make_command(cat, evt):
                    return lambda: self._test_event_from_file(cat, evt)

                btn = tk.Button(
                    button_frame,
                    text=event_name,
                    command=make_command(category, event_name),
                    width=18
                )
                btn.pack(side=tk.LEFT, padx=(0, 5))

            row += 1

        return frame

    def _test_event_from_file(self, category, event_name):
        """Load a real journal event JSON from category/event path and process it"""
        log_debug(f"DEBUG: Button clicked for {category}/{event_name}")

        if not self.journal_processor:
            log_debug("DEBUG ERROR: No journal processor available!")
            return

        file_path = os.path.join(DEBUG_DATA_DIR, category.lower(), f"{event_name}.json")

        if not os.path.exists(file_path):
            log_debug(f"DEBUG FILE MISSING: {file_path}")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                mock_entry = json.load(f)
        except Exception as e:
            log_debug(f"Failed to load {file_path}: {e}")
            return

        # The journal processor expects the actual journal field names, not abstract names
        # So we don't need to transform anything - just use the original entry
        transformed_entry = mock_entry

        # Mocked game state
        mock_state = {
            "Credits": 1000000,
            "IsDocked": True
        }

        result = self.journal_processor.process_journal_entry(
            cmdr="TestCommander",
            is_beta=False,
            system="Test System",
            station="Test Station",
            entry=transformed_entry,
            state=mock_state
        )

        log_debug(f"DEBUG: Test result: {result}")

        # Trigger UI refresh if available
        if hasattr(self.income_tracker, 'update_window'):
            self.income_tracker.update_window()

        # Also refresh the UI display to show updated values
        if hasattr(self.income_tracker, 'ui') and hasattr(self.income_tracker.ui, 'update_display'):
            self.income_tracker.ui.update_display()
