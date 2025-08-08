"""
EDMC Income Tracker Plugin - User Interface components
"""

import tkinter as tk
from l10n import Locale
from utils import log_debug, log_warning

class IncomeTrackerUI:
    """Manages the main application UI"""

    def __init__(self, income_tracker, preferences_manager):
        self.income_tracker = income_tracker
        self.preferences = preferences_manager

    def create_main_ui(self, parent):
        """Create the main application UI"""
        frame = tk.Frame(parent)

        # Set up column weights to eliminate right edge padding
        frame.columnconfigure(1, weight=0)  # Middle column gets no weight
        frame.columnconfigure(2, weight=1)  # Right column gets all the weight

        # Header
        self._create_header(frame)

        # Income display
        self._create_income_display(frame)

        # Category breakdown
        self._create_category_breakdown(frame)

        # Update display
        self.income_tracker.update_window()

        return frame

    def update_display(self):
        """Update the display with current income data"""
        log_debug("update_display() called")

        if not self.income_tracker:
            return

        # Update speed widget
        if self.speed_widget:
            speed = self.income_tracker.speed()
            msg = f"{Locale.string_from_number(speed, 2)} Cr/hr"
            self.speed_widget.after(0, self.speed_widget.config, {"text": msg})
        else:
            log_warning("speed_widget is None")

        # Update earned widget (total income)
        if self.earned_widget:
            # Calculate total based on Show preferences
            total = 0.0

            # Only include earnings from categories that are being tracked
            if self.preferences.cached_track_trading:
                total += self.income_tracker.trip_earnings_by_category("trading")
            if self.preferences.cached_track_combat:
                total += self.income_tracker.trip_earnings_by_category("combat")
            if self.preferences.cached_track_exploration:
                total += self.income_tracker.trip_earnings_by_category("exploration")
            if self.preferences.cached_track_missions:
                total += self.income_tracker.trip_earnings_by_category("missions")
            # Credits are shown separately, not included in session total

            # Add saved earnings (always included)
            total += self.income_tracker.saved_earnings

            # Subtract maintenance costs if tracking is enabled
            if self.preferences.cached_track_maintenance:
                maintenance = self.income_tracker.trip_earnings_by_category("maintenance")
                total += maintenance  # maintenance is already negative

            msg = f"{Locale.string_from_number(total, 2)} Cr"
            self.earned_widget.after(0, self.earned_widget.config, {"text": msg})
        else:
            log_warning("earned_widget is None")

        # Update category breakdown
        self._update_category_widgets()

        log_debug("Display updated")

    def update_breakdown_visibility(self):
        """Update the visibility of the entire category breakdown section"""
        if self.trading_widget:
            parent = self.trading_widget.master
            show_breakdown = self.show_breakdown.get()

            # Find all category widgets and their labels
            for child in parent.winfo_children():
                if isinstance(child, tk.Label):
                    if any(cat in child.cget("text") for cat in ["Trading", "Combat", "Exploration", "Missions"]):
                        if "Trading" in child.cget("text"):
                            child.grid() if (show_breakdown and self.preferences.cached_track_trading) else child.grid_remove()
                        elif "Combat" in child.cget("text"):
                            child.grid() if (show_breakdown and self.preferences.cached_track_combat) else child.grid_remove()
                        elif "Exploration" in child.cget("text"):
                            child.grid() if (show_breakdown and self.preferences.cached_track_exploration) else child.grid_remove()
                        elif "Missions" in child.cget("text"):
                            child.grid() if (show_breakdown and self.preferences.cached_track_missions) else child.grid_remove()

            # Update widget visibility
            if self.trading_widget:
                self.trading_widget.grid() if (show_breakdown and self.preferences.cached_track_trading) else self.trading_widget.grid_remove()
            if self.combat_widget:
                self.combat_widget.grid() if (show_breakdown and self.preferences.cached_track_combat) else self.combat_widget.grid_remove()
            if self.exploration_widget:
                self.exploration_widget.grid() if (show_breakdown and self.preferences.cached_track_exploration) else self.exploration_widget.grid_remove()
            if self.missions_widget:
                self.missions_widget.grid() if (show_breakdown and self.preferences.cached_track_missions) else self.missions_widget.grid_remove()

    def _create_header(self, frame):
        """Create the header section"""
        # Title
        title_label = tk.Label(frame, text="Income Tracker", font=("Arial", 10, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        # Reset button aligned to the right of the title
        reset_btn = tk.Button(frame, text="Reset", command=self.income_tracker.reset)
        reset_btn.grid(row=0, column=2, sticky=tk.E, pady=(0, 5))

    def _create_category_row(self, frame, title, category, row, default_text="0 Cr"):
        """Create a category row with label and widget"""
        # Create label
        label = tk.Label(frame, text=title, justify=tk.LEFT)
        label.grid(row=row, column=0, sticky=tk.W, padx=(0, 5))

        # Create widget
        widget = tk.Label(frame, text=default_text, justify=tk.RIGHT, font=("Arial", 9))
        widget.grid(row=row, column=2, sticky=tk.E, padx=(5, 0))

        # Store references
        setattr(self, f'{category}_label', label)
        setattr(self, f'{category}_widget', widget)

        return label, widget

    def _create_income_display(self, frame):
        """Create the main income display section"""
        # Create income display rows
        self._create_category_row(frame, "Hourly", "speed", 1, "0 Cr/hr")
        self._create_category_row(frame, "Income", "earned", 2)
        self._create_category_row(frame, "Maintenance", "maintenance", 3)

        # Category breakdown toggle
        self.show_breakdown = tk.BooleanVar(value=False)
        breakdown_toggle = tk.Checkbutton(frame, text="Income Breakdown",
                                        variable=self.show_breakdown,
                                        command=self.income_tracker.update_breakdown_visibility,
                                        foreground="#ff8000")
        breakdown_toggle.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))

    def _create_category_breakdown(self, frame):
        """Create the category breakdown section"""
        # Create all category rows
        self._create_category_row(frame, "Trading", "trading", 5)
        self._create_category_row(frame, "Combat", "combat", 6)
        self._create_category_row(frame, "Exploration", "exploration", 7)
        self._create_category_row(frame, "Missions", "missions", 8)

        # Set initial visibility based on breakdown toggle
        if self.show_breakdown.get():
            # Show all breakdown items
            pass  # Already visible by default
        else:
            # Hide all breakdown items
            self.trading_label.grid_remove()
            self.trading_widget.grid_remove()
            self.combat_label.grid_remove()
            self.combat_widget.grid_remove()
            self.exploration_label.grid_remove()
            self.exploration_widget.grid_remove()
            self.missions_label.grid_remove()
            self.missions_widget.grid_remove()

    def _update_category_widgets(self):
        """Update category-specific widgets"""
        if self.trading_widget and self.preferences.cached_track_trading:
            trading_total = self.income_tracker.trip_earnings_by_category("trading")
            msg = f"{Locale.string_from_number(trading_total, 2)} Cr"
            self.trading_widget.after(0, self.trading_widget.config, {"text": msg})

        if self.combat_widget and self.preferences.cached_track_combat:
            combat_total = self.income_tracker.trip_earnings_by_category("combat")
            msg = f"{Locale.string_from_number(combat_total, 2)} Cr"
            self.combat_widget.after(0, self.combat_widget.config, {"text": msg})

        if self.exploration_widget and self.preferences.cached_track_exploration:
            exploration_total = self.income_tracker.trip_earnings_by_category("exploration")
            msg = f"{Locale.string_from_number(exploration_total, 2)} Cr"
            self.exploration_widget.after(0, self.exploration_widget.config, {"text": msg})

        if self.missions_widget and self.preferences.cached_track_missions:
            missions_total = self.income_tracker.trip_earnings_by_category("missions")
            msg = f"{Locale.string_from_number(missions_total, 2)} Cr"
            self.missions_widget.after(0, self.missions_widget.config, {"text": msg})

        if self.maintenance_widget and self.preferences.cached_track_maintenance:
            maintenance_total = self.income_tracker.trip_earnings_by_category("maintenance")
            msg = f"{Locale.string_from_number(maintenance_total, 2)} Cr"
            self.maintenance_widget.after(0, self.maintenance_widget.config, {"text": msg})
