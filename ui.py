"""
EDMC Income Tracker Plugin - User Interface components
"""

import tkinter as tk
from l10n import Locale
from utils import log_debug, log_warning, DEBUG_MODE

class IncomeTrackerUI:
    """Manages the main application UI"""

    def __init__(self, income_tracker, preferences_manager):
        self.income_tracker = income_tracker
        self.preferences = preferences_manager

        # Widget references
        self.speed_widget = None
        self.earned_widget = None
        self.trading_widget = None
        self.combat_widget = None
        self.exploration_widget = None
        self.missions_widget = None
        self.credits_widget = None
        self.show_breakdown = None

        # Category labels
        self.trading_label = None
        self.combat_label = None
        self.exploration_label = None
        self.missions_label = None
        self.credits_label = None

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

        # Debug section
        if DEBUG_MODE:
            self._create_debug_section(frame)

        # Update display
        self.income_tracker.update_window()

        return frame

    def _create_header(self, frame):
        """Create the header section"""
        # Title
        title_label = tk.Label(frame, text="Income Tracker", font=("Arial", 10, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        # Reset button aligned to the right of the title
        reset_btn = tk.Button(frame, text="Reset", command=self.income_tracker.reset)
        reset_btn.grid(row=0, column=2, sticky=tk.E, pady=(0, 5))

    def _create_income_display(self, frame):
        """Create the main income display section"""
        # Hourly Income display
        speed_label = tk.Label(frame, text="Hourly", justify=tk.LEFT)
        speed_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 5))

        self.speed_widget = tk.Label(frame, text="0 Cr/hr", justify=tk.RIGHT, font=("Arial", 9))
        self.speed_widget.grid(row=1, column=2, sticky=tk.E, padx=(5, 0))

        # Total Income display
        earned_label = tk.Label(frame, text="This Session", justify=tk.LEFT)
        earned_label.grid(row=2, column=0, sticky=tk.W, padx=(0, 5))

        self.earned_widget = tk.Label(frame, text="0 Cr", justify=tk.RIGHT, font=("Arial", 9))
        self.earned_widget.grid(row=2, column=2, sticky=tk.E, padx=(5, 0))

        # Credits display (outside breakdown)
        self.credits_label = tk.Label(frame, text="Total Credits", justify=tk.LEFT)
        self.credits_label.grid(row=3, column=0, sticky=tk.W, padx=(0, 5))

        self.credits_widget = tk.Label(frame, text="0 Cr", justify=tk.RIGHT, font=("Arial", 9))
        self.credits_widget.grid(row=3, column=2, sticky=tk.E, padx=(5, 0))

        # Category breakdown toggle
        self.show_breakdown = tk.BooleanVar(value=False)
        breakdown_toggle = tk.Checkbutton(frame, text="Income Breakdown",
                                        variable=self.show_breakdown,
                                        command=self.income_tracker.update_breakdown_visibility,
                                        foreground="#ff8000")
        breakdown_toggle.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))

    def _create_category_breakdown(self, frame):
        """Create the category breakdown section"""
        row = 5

        # Trading display
        self.trading_label = tk.Label(frame, text="Trading:", justify=tk.LEFT)
        self.trading_label.grid(row=row, column=0, sticky=tk.W, padx=(0, 5))
        self.trading_widget = tk.Label(frame, text="0 Cr", justify=tk.RIGHT, font=("Arial", 9))
        self.trading_widget.grid(row=row, column=2, sticky=tk.E, padx=(5, 0))
        self._set_category_visibility("trading", row)
        row += 1

        # Combat display
        self.combat_label = tk.Label(frame, text="Combat:", justify=tk.LEFT)
        self.combat_label.grid(row=row, column=0, sticky=tk.W, padx=(0, 5))
        self.combat_widget = tk.Label(frame, text="0 Cr", justify=tk.RIGHT, font=("Arial", 9))
        self.combat_widget.grid(row=row, column=2, sticky=tk.E, padx=(5, 0))
        self._set_category_visibility("combat", row)
        row += 1

        # Exploration display
        self.exploration_label = tk.Label(frame, text="Exploration:", justify=tk.LEFT)
        self.exploration_label.grid(row=row, column=0, sticky=tk.W, padx=(0, 5))
        self.exploration_widget = tk.Label(frame, text="0 Cr", justify=tk.RIGHT, font=("Arial", 9))
        self.exploration_widget.grid(row=row, column=2, sticky=tk.E, padx=(5, 0))
        self._set_category_visibility("exploration", row)
        row += 1

        # Missions display
        self.missions_label = tk.Label(frame, text="Missions:", justify=tk.LEFT)
        self.missions_label.grid(row=row, column=0, sticky=tk.W, padx=(0, 5))
        self.missions_widget = tk.Label(frame, text="0 Cr", justify=tk.RIGHT, font=("Arial", 9))
        self.missions_widget.grid(row=row, column=2, sticky=tk.E, padx=(5, 0))
        self._set_category_visibility("missions", row)
        row += 1



    def _create_debug_section(self, frame):
        """Create debug section for testing"""
        button_frame = tk.Frame(frame)
        button_frame.grid(row=10, column=0, columnspan=3, pady=(10, 0))

        # Test button to simulate a transaction
        test_btn = tk.Button(button_frame, text="Test (+1000 Cr)",
                           command=lambda: self.income_tracker.transaction(1000, "trading"))
        test_btn.grid(row=0, column=1, sticky=tk.W)

        # Test button to simulate credits
        credits_btn = tk.Button(button_frame, text="Test Credits (+500 Cr)",
                              command=lambda: self.income_tracker.transaction(500, "credits"))
        credits_btn.grid(row=0, column=2, sticky=tk.W)

        # Test button to simulate Credits journal event
        credits_event_btn = tk.Button(button_frame, text="Test Credits Event",
                                    command=lambda: self._test_credits_event())
        credits_event_btn.grid(row=1, column=1, sticky=tk.W)

    def _test_credits_event(self):
        """Test function to simulate a Credits journal event"""
        test_entry = {
            "event": "Credits",
            "Change": 1000,
            "Balance": 50000
        }
        # Simulate processing the event
        if "Change" in test_entry:
            change = test_entry["Change"]
            self.income_tracker.transaction(change, "credits")

    def _set_category_visibility(self, category, row):
        """Set initial visibility for a category based on preferences"""
        show_setting = getattr(self.preferences, f'cached_show_{category}')
        if show_setting and self.show_breakdown.get():
            getattr(self, f'{category}_label').grid()
            getattr(self, f'{category}_widget').grid()
        else:
            getattr(self, f'{category}_label').grid_remove()
            getattr(self, f'{category}_widget').grid_remove()

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

            # Only include earnings from categories that are set to show
            if self.preferences.cached_show_trading:
                total += self.income_tracker.trip_earnings_by_category("trading")
            if self.preferences.cached_show_combat:
                total += self.income_tracker.trip_earnings_by_category("combat")
            if self.preferences.cached_show_exploration:
                total += self.income_tracker.trip_earnings_by_category("exploration")
            if self.preferences.cached_show_missions:
                total += self.income_tracker.trip_earnings_by_category("missions")
            # Credits are shown separately, not included in session total

            # Add saved earnings (always included)
            total += self.income_tracker.saved_earnings

            msg = f"{Locale.string_from_number(total, 2)} Cr"
            self.earned_widget.after(0, self.earned_widget.config, {"text": msg})
        else:
            log_warning("earned_widget is None")

        # Update category breakdown
        self._update_category_widgets()

        log_debug("Display updated")

    def _update_credits_from_state(self):
        """Update credits display from state data if available"""
        # This will be called from journal_processor when state is available
        pass

    def update_credits_from_state(self, credits_balance):
        """Update credits display with balance from state"""
        if self.credits_widget and credits_balance is not None:
            msg = f"{Locale.string_from_number(credits_balance, 2)} Cr"
            log_debug(f"Updating credits from state: {msg}")
            self.credits_widget.after(0, self.credits_widget.config, {"text": msg})

    def _update_category_widgets(self):
        """Update category-specific widgets"""
        if self.trading_widget and self.preferences.cached_show_trading:
            trading_total = self.income_tracker.trip_earnings_by_category("trading")
            msg = f"{Locale.string_from_number(trading_total, 2)} Cr"
            self.trading_widget.after(0, self.trading_widget.config, {"text": msg})

        if self.combat_widget and self.preferences.cached_show_combat:
            combat_total = self.income_tracker.trip_earnings_by_category("combat")
            msg = f"{Locale.string_from_number(combat_total, 2)} Cr"
            self.combat_widget.after(0, self.combat_widget.config, {"text": msg})

        if self.exploration_widget and self.preferences.cached_show_exploration:
            exploration_total = self.income_tracker.trip_earnings_by_category("exploration")
            msg = f"{Locale.string_from_number(exploration_total, 2)} Cr"
            self.exploration_widget.after(0, self.exploration_widget.config, {"text": msg})

        if self.missions_widget and self.preferences.cached_show_missions:
            missions_total = self.income_tracker.trip_earnings_by_category("missions")
            msg = f"{Locale.string_from_number(missions_total, 2)} Cr"
            self.missions_widget.after(0, self.missions_widget.config, {"text": msg})

        if self.credits_widget:
            credits_total = self.income_tracker.trip_earnings_by_category("credits")
            msg = f"{Locale.string_from_number(credits_total, 2)} Cr"
            self.credits_widget.after(0, self.credits_widget.config, {"text": msg})

    def update_widget_visibility(self):
        """Update the visibility of category widgets based on Show settings"""
        if self.trading_widget:
            parent = self.trading_widget.master
            # Find all widgets in the frame and update their visibility
            for child in parent.winfo_children():
                if isinstance(child, tk.Label):
                    if "Trading:" in child.cget("text"):
                        child.grid() if self.preferences.cached_show_trading else child.grid_remove()
                    elif "Combat:" in child.cget("text"):
                        child.grid() if self.preferences.cached_show_combat else child.grid_remove()
                    elif "Exploration:" in child.cget("text"):
                        child.grid() if self.preferences.cached_show_exploration else child.grid_remove()
                    elif "Missions:" in child.cget("text"):
                        child.grid() if self.preferences.cached_show_missions else child.grid_remove()

            # Update widget visibility
            if self.trading_widget:
                self.trading_widget.grid() if self.preferences.cached_show_trading else self.trading_widget.grid_remove()
            if self.combat_widget:
                self.combat_widget.grid() if self.preferences.cached_show_combat else self.combat_widget.grid_remove()
            if self.exploration_widget:
                self.exploration_widget.grid() if self.preferences.cached_show_exploration else self.exploration_widget.grid_remove()
            if self.missions_widget:
                self.missions_widget.grid() if self.preferences.cached_show_missions else self.missions_widget.grid_remove()



    def update_breakdown_visibility(self):
        """Update the visibility of the entire category breakdown section"""
        if self.trading_widget:
            parent = self.trading_widget.master
            show_breakdown = self.show_breakdown.get()

            # Find all category widgets and their labels
            for child in parent.winfo_children():
                if isinstance(child, tk.Label):
                    if any(cat in child.cget("text") for cat in ["Trading:", "Combat:", "Exploration:", "Missions:"]):
                        if "Trading:" in child.cget("text"):
                            child.grid() if (show_breakdown and self.preferences.cached_show_trading) else child.grid_remove()
                        elif "Combat:" in child.cget("text"):
                            child.grid() if (show_breakdown and self.preferences.cached_show_combat) else child.grid_remove()
                        elif "Exploration:" in child.cget("text"):
                            child.grid() if (show_breakdown and self.preferences.cached_show_exploration) else child.grid_remove()
                        elif "Missions:" in child.cget("text"):
                            child.grid() if (show_breakdown and self.preferences.cached_show_missions) else child.grid_remove()

            # Update widget visibility
            if self.trading_widget:
                self.trading_widget.grid() if (show_breakdown and self.preferences.cached_show_trading) else self.trading_widget.grid_remove()
            if self.combat_widget:
                self.combat_widget.grid() if (show_breakdown and self.preferences.cached_show_combat) else self.combat_widget.grid_remove()
            if self.exploration_widget:
                self.exploration_widget.grid() if (show_breakdown and self.preferences.cached_show_exploration) else self.exploration_widget.grid_remove()
            if self.missions_widget:
                self.missions_widget.grid() if (show_breakdown and self.preferences.cached_show_missions) else self.missions_widget.grid_remove()
