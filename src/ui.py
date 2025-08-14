"""
EDMC Income Tracker Plugin - Main UI
"""

import tkinter as tk
from l10n import Locale # type: ignore
from src.utils import log_debug
from src.constants import UI_ELEMENT_STATES, DEBUG_MODE


class IncomeTrackerUI:
    """Manages the main application UI"""

    def __init__(self, income_tracker, preferences_manager, journal_processor=None):
        self.income_tracker = income_tracker
        self.preferences = preferences_manager
        self.journal_processor = journal_processor

    #region UI creation helpers
    def _create_title_and_reset(self, frame):
        self.title_label = tk.Label(frame, text="Income Tracker", font=("Euro Caps", 10, "bold"))
        self.title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.reset_btn = tk.Button(frame, text="Reset", command=self.income_tracker.reset)
        self.reset_btn.grid(row=0, column=2, sticky=tk.E, pady=(0, 5))

    def _create_income_row(self, frame, title, category, row, default_text="0 Cr"):
        label = tk.Label(frame, text=title, justify=tk.LEFT)
        label.grid(row=row, column=0, sticky=tk.W, padx=(0, 5))

        widget = tk.Label(frame, text=default_text, justify=tk.RIGHT)
        widget.grid(row=row, column=2, sticky=tk.E, padx=(5, 0))

        setattr(self, f'{category}_label', label)
        setattr(self, f'{category}_widget', widget)

    def _create_breakdown_toggle(self, frame, row):
        self.show_breakdown = tk.BooleanVar(value=False)
        self.breakdown_toggle = tk.Checkbutton(
            frame,
            text="Income Breakdown",
            variable=self.show_breakdown,
            command=self.refresh_ui,
            foreground="#ff8000"
        )
        self.breakdown_toggle.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
    #endregion

    #region Element visibility
    def _should_show_element(self, name):
        state = UI_ELEMENT_STATES.get(name)
        if not state:
            return False

        # Always show?
        if state.get("always_show"):
            return True

        # View mode check
        if "show_in" in state and self.preferences.cached_view_mode not in state["show_in"]:
            return False

        # Enabled flag check (dynamic mapping)
        if "enabled" in state:
            pref_attr = f"cached_{state['enabled']}"
            if not getattr(self.preferences, pref_attr, False):
                return False

        # Requirement check (maps directly to UI attributes)
        if "requires" in state:
            req_attr = state["requires"]
            req_value = getattr(self, req_attr, None)
            if isinstance(req_value, tk.BooleanVar):
                if not req_value.get():
                    return False
            elif not req_value:  # Covers missing attributes
                return False

        return True


    def _toggle_element(self, element, visible):
        if visible:
            element.grid()
        else:
            element.grid_remove()

    def _update_element_visibility(self, force_hide=False):
        for name in UI_ELEMENT_STATES:
            visible = False if force_hide else self._should_show_element(name)
            label = getattr(self, f'{name}_label', None)
            widget = getattr(self, f'{name}_widget', None)
            element = getattr(self, name, None)

            if label and widget:  # paired
                self._toggle_element(label, visible)
                self._toggle_element(widget, visible)
            elif label:  # single label
                self._toggle_element(label, visible)
            elif element:  # single widget/control
                self._toggle_element(element, visible)
    #endregion

    #region Main UI build
    def create_main_ui(self, parent):
        frame = tk.Frame(parent)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=1)

        self._create_title_and_reset(frame)

        rows = [
            ("Hourly", "speed", "0 Cr/hr"),
            ("Income", "earned"),
            ("Maintenance", "maintenance"),
            ("Total", "total_credits"),
        ]
        for i, (title, cat, *default) in enumerate(rows, start=1):
            self._create_income_row(frame, title, cat, i, *default)

        self._create_breakdown_toggle(frame, 5)

        categories = ["trading", "combat", "exploration", "missions"]
        for i, cat in enumerate(categories, start=6):
            self._create_income_row(frame, cat.capitalize(), cat, i)

        # Make sure the income labels are up-to-date
        self._update_element_visibility()
        self.income_tracker.update_window()

        # --- DEBUG MODE ---

        if DEBUG_MODE:
            log_debug("DEBUG: DEBUG_MODE is True, creating debug interface")
            from src.debug.debug import DebugInterface
            debug_ui = DebugInterface(
                journal_processor=self.journal_processor,
                income_tracker=self.income_tracker
            )
            debug_frame = debug_ui.create_debug_frame(frame)
            debug_frame.grid(row=99, column=0, columnspan=3, pady=(10, 0), sticky=tk.W)
            log_debug("DEBUG: Debug interface created and added to UI")
        else:
            log_debug("DEBUG: DEBUG_MODE is False, skipping debug interface")

        return frame
    #endregion

    #region Display updates
    def update_display(self):
        log_debug("update_display() called")
        if not self.income_tracker:
            return

        if any([
            self.preferences.cached_track_trading,
            self.preferences.cached_track_combat,
            self.preferences.cached_track_exploration,
            self.preferences.cached_track_missions
        ]):
            self._update_element_visibility()
            self._update_all_values()
        else:
            self._show_no_sources_message()

        log_debug("Display updated")

    def _show_no_sources_message(self):
        self._update_element_visibility(force_hide=True)
        if not hasattr(self, 'no_sources_label'):
            parent = getattr(self, 'title_label', None).master if hasattr(self, 'title_label') else None
            if parent:
                self.no_sources_label = tk.Label(parent, text="No income sources are tracked")
        self.no_sources_label.grid(row=1, column=0, columnspan=3, pady=(5, 10), sticky=tk.W)

    def _update_all_values(self):
        if hasattr(self, 'speed_widget'):
            speed = self.income_tracker.speed()
            self.speed_widget.after(0, self.speed_widget.config, {"text": f"{Locale.string_from_number(speed, 2)} Cr/hr"})

        total = sum(
            self.income_tracker.trip_earnings_by_category(cat)
            for cat, track in [
                ("trading", self.preferences.cached_track_trading),
                ("combat", self.preferences.cached_track_combat),
                ("exploration", self.preferences.cached_track_exploration),
                ("missions", self.preferences.cached_track_missions)
            ] if track
        ) + self.income_tracker.saved_earnings + self.income_tracker.trip_earnings_by_category("maintenance")

        if hasattr(self, 'earned_widget'):
            self.earned_widget.after(0, self.earned_widget.config, {"text": f"{Locale.string_from_number(total, 2)} Cr"})

        if hasattr(self, 'maintenance_widget'):
            maint = self.income_tracker.trip_earnings_by_category("maintenance")
            self.maintenance_widget.after(0, self.maintenance_widget.config, {"text": f"{Locale.string_from_number(maint, 2)} Cr"})

        if hasattr(self, 'total_credits_widget'):
            credits = self.income_tracker.get_current_credits()
            self.total_credits_widget.after(0, self.total_credits_widget.config, {"text": f"{Locale.string_from_number(credits, 0)} Cr"})

        self._update_category_widgets()

    def _update_category_widgets(self):
        for cat, track in [
            ("trading", self.preferences.cached_track_trading),
            ("combat", self.preferences.cached_track_combat),
            ("exploration", self.preferences.cached_track_exploration),
            ("missions", self.preferences.cached_track_missions)
        ]:
            widget = getattr(self, f"{cat}_widget", None)
            if widget and track:
                value = self.income_tracker.trip_earnings_by_category(cat)
                widget.after(0, widget.config, {"text": f"{Locale.string_from_number(value, 2)} Cr"})

    def refresh_ui(self):
        log_debug("Refreshing UI visibility")
        self._update_element_visibility()
        self._update_category_widgets()
    #endregion
