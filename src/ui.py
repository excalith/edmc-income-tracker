"""
EDMC Income Tracker Plugin - User Interface components
"""

import tkinter as tk
from l10n import Locale
from src.utils import log_debug, log_warning

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

        # Create all UI sections
        self._create_header(frame)
        self._create_income_display(frame)
        self._create_category_breakdown(frame)

        # Apply initial view mode
        self._apply_view_mode()

        # Update display
        self.income_tracker.update_window()

        return frame

    def update_display(self):
        """Update the display with current income data"""
        log_debug("update_display() called")

        if not self.income_tracker:
            return

        # Check if any income sources are tracked
        has_income_sources = (
            self.preferences.cached_track_trading or
            self.preferences.cached_track_combat or
            self.preferences.cached_track_exploration or
            self.preferences.cached_track_missions
        )

        if has_income_sources:
            # Show normal UI elements
            self._show_income_ui()
            self._update_income_values()
        else:
            # Show "no sources" message
            self._show_no_sources_message()

        log_debug("Display updated")

    def update_breakdown_visibility(self):
        """Update the visibility of the entire category breakdown section"""
        if self.show_breakdown.get():
            self._show_category_breakdown()
        else:
            self._hide_category_breakdown()

    def _apply_view_mode(self):
        """Apply the current view mode (compact or full)"""
        if self.preferences.cached_view_mode == "compact":
            self._apply_compact_view()
        else:
            self._apply_full_view()

    def _apply_compact_view(self):
        """Apply compact view mode - show only essential elements"""
        # Always show header (title + reset)
        if hasattr(self, 'title_label'):
            self.title_label.grid()
        if hasattr(self, 'reset_btn'):
            self.reset_btn.grid()

        # Show only essential income info
        if hasattr(self, 'speed_label') and hasattr(self, 'speed_widget'):
            self.speed_label.grid()
            self.speed_widget.grid()
        if hasattr(self, 'earned_label') and hasattr(self, 'earned_widget'):
            self.earned_label.grid()
            self.earned_widget.grid()

        # Hide maintenance and breakdown in compact mode
        if hasattr(self, 'maintenance_label') and hasattr(self, 'maintenance_widget'):
            self.maintenance_label.grid_remove()
            self.maintenance_widget.grid_remove()

        # Hide total credits in compact mode (or if preference disabled)
        if hasattr(self, 'total_credits_label') and hasattr(self, 'total_credits_widget'):
            self.total_credits_label.grid_remove()
            self.total_credits_widget.grid_remove()

        # Hide the breakdown toggle checkbox
        if hasattr(self, 'show_breakdown'):
            # Find and hide the checkbox widget
            for child in self.title_label.master.winfo_children():
                if isinstance(child, tk.Checkbutton) and child.cget('text') == 'Income Breakdown':
                    child.grid_remove()
                    break

        # Hide all category breakdown elements
        self._hide_category_breakdown()

    def _apply_full_view(self):
        """Apply full view mode - show all elements"""
        # Always show header
        if hasattr(self, 'title_label'):
            self.title_label.grid()
        if hasattr(self, 'reset_btn'):
            self.reset_btn.grid()

        # Show all income elements
        if hasattr(self, 'speed_label') and hasattr(self, 'speed_widget'):
            self.speed_label.grid()
            self.speed_widget.grid()
        if hasattr(self, 'earned_label') and hasattr(self, 'earned_widget'):
            self.earned_label.grid()
            self.earned_widget.grid()
        if hasattr(self, 'maintenance_label') and hasattr(self, 'maintenance_widget'):
            self.maintenance_label.grid()
            self.maintenance_widget.grid()

        # Show total credits in full view (only if preference allows)
        if hasattr(self, 'total_credits_label') and hasattr(self, 'total_credits_widget'):
            if self.preferences.cached_show_total_credits:
                self.total_credits_label.grid()
                self.total_credits_widget.grid()
            else:
                self.total_credits_label.grid_remove()
                self.total_credits_widget.grid_remove()

        # Show the breakdown toggle checkbox
        if hasattr(self, 'show_breakdown'):
            # Find and show the checkbox widget
            for child in self.title_label.master.winfo_children():
                if isinstance(child, tk.Checkbutton) and child.cget('text') == 'Income Breakdown':
                    child.grid()
                    break

        # Show/hide category breakdown based on toggle state
        if hasattr(self, 'show_breakdown') and self.show_breakdown.get():
            self._show_category_breakdown()
        else:
            self._hide_category_breakdown()

    def _create_header(self, frame):
        """Create the header section"""
        # Title
        self.title_label = tk.Label(frame, text="Income Tracker", font=("Euro Caps", 10, "bold"))
        self.title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        # Reset button aligned to the right of the title
        self.reset_btn = tk.Button(frame, text="Reset", command=self.income_tracker.reset)
        self.reset_btn.grid(row=0, column=2, sticky=tk.E, pady=(0, 5))

    def _create_category_row(self, frame, title, category, row, default_text="0 Cr"):
        """Create a category row with label and widget"""
        # Create label
        label = tk.Label(frame, text=title, justify=tk.LEFT)
        label.grid(row=row, column=0, sticky=tk.W, padx=(0, 5))

        # Create widget
        widget = tk.Label(frame, text=default_text, justify=tk.RIGHT)
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

        # Total Credits (between Maintenance and Income Breakdown)
        self._create_category_row(frame, "Total", "total_credits", 4, "0 Cr")
        # Set initial visibility based on preference
        if not self.preferences.cached_show_total_credits:
            self.total_credits_label.grid_remove()
            self.total_credits_widget.grid_remove()

        # Category breakdown toggle
        self.show_breakdown = tk.BooleanVar(value=False)
        breakdown_toggle = tk.Checkbutton(frame, text="Income Breakdown",
                                        variable=self.show_breakdown,
                                        command=self.income_tracker.update_breakdown_visibility,
                                        foreground="#ff8000")
        breakdown_toggle.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))

    def _create_category_breakdown(self, frame):
        """Create the category breakdown section"""
        # Create all category rows
        self._create_category_row(frame, "Trading", "trading", 6)
        self._create_category_row(frame, "Combat", "combat", 7)
        self._create_category_row(frame, "Exploration", "exploration", 8)
        self._create_category_row(frame, "Missions", "missions", 9)

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

        if self.maintenance_widget:
            maintenance_total = self.income_tracker.trip_earnings_by_category("maintenance")
            msg = f"{Locale.string_from_number(maintenance_total, 2)} Cr"
            self.maintenance_widget.after(0, self.maintenance_widget.config, {"text": msg})

        # Update Total Credits
        if hasattr(self, 'total_credits_widget'):
            current_credits = self.income_tracker.get_current_credits()
            msg = f"{Locale.string_from_number(current_credits, 0)} Cr"
            self.total_credits_widget.after(0, self.total_credits_widget.config, {"text": msg})

    def _show_income_ui(self):
        """Show the normal income UI elements"""
        # Hide no sources message first to avoid layout conflicts
        if hasattr(self, 'no_sources_label'):
            self.no_sources_label.grid_remove()

        # Apply the current view mode
        self._apply_view_mode()

    def _show_no_sources_message(self):
        """Show the 'no income sources' message"""
        # Hide all main elements
        if hasattr(self, 'reset_btn'):
            self.reset_btn.grid_remove()
        if hasattr(self, 'speed_label') and hasattr(self, 'speed_widget'):
            self.speed_label.grid_remove()
            self.speed_widget.grid_remove()
        if hasattr(self, 'earned_label') and hasattr(self, 'earned_widget'):
            self.earned_label.grid_remove()
            self.earned_widget.grid_remove()
        if hasattr(self, 'maintenance_label') and hasattr(self, 'maintenance_widget'):
            self.maintenance_label.grid_remove()
            self.maintenance_widget.grid_remove()

        # Hide total credits
        if hasattr(self, 'total_credits_label') and hasattr(self, 'total_credits_widget'):
            self.total_credits_label.grid_remove()
            self.total_credits_widget.grid_remove()

        # Hide the breakdown toggle checkbox
        if hasattr(self, 'show_breakdown'):
            # Find and hide the checkbox widget
            for child in self.title_label.master.winfo_children():
                if isinstance(child, tk.Checkbutton) and child.cget('text') == 'Income Breakdown':
                    child.grid_remove()
                    break

        # Hide all category breakdown elements
        self._hide_category_breakdown()

        # Show no sources message at the top (row 1) to avoid overlap
        if not hasattr(self, 'no_sources_label'):
            # Create the message if it doesn't exist
            parent = self.title_label.master if hasattr(self, 'title_label') else None
            if parent:
                self.no_sources_label = tk.Label(parent, text="No income sources are tracked")
                self.no_sources_label.grid(row=1, column=0, columnspan=3, pady=(5, 10), sticky=tk.W)
        else:
            self.no_sources_label.grid(row=1, column=0, columnspan=3, pady=(5, 10), sticky=tk.W)

    def _hide_category_breakdown(self):
        """Hide all category breakdown elements"""
        for category in ['trading', 'combat', 'exploration', 'missions']:
            if hasattr(self, f'{category}_label') and hasattr(self, f'{category}_widget'):
                getattr(self, f'{category}_label').grid_remove()
                getattr(self, f'{category}_widget').grid_remove()

    def _show_category_breakdown(self):
        """Show category breakdown elements based on tracking preferences"""
        for category in ['trading', 'combat', 'exploration', 'missions']:
            if hasattr(self, f'{category}_label') and hasattr(self, f'{category}_widget'):
                # Only show if this category is being tracked
                is_tracked = getattr(self.preferences, f'cached_track_{category}')
                if is_tracked:
                    getattr(self, f'{category}_label').grid()
                    getattr(self, f'{category}_widget').grid()
                else:
                    getattr(self, f'{category}_label').grid_remove()
                    getattr(self, f'{category}_widget').grid_remove()

    def _update_income_values(self):
        """Update all income-related values"""
        # Update speed widget
        if self.speed_widget:
            speed = self.income_tracker.speed()
            msg = f"{Locale.string_from_number(speed, 2)} Cr/hr"
            self.speed_widget.after(0, self.speed_widget.config, {"text": msg})

        # Update earned widget (total income)
        if self.earned_widget:
            # Calculate total based on tracking preferences
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

            # Add saved earnings (always included)
            total += self.income_tracker.saved_earnings

            # Always subtract maintenance costs (maintenance is always tracked)
            maintenance = self.income_tracker.trip_earnings_by_category("maintenance")
            total += maintenance  # maintenance is already negative

            msg = f"{Locale.string_from_number(total, 2)} Cr"
            self.earned_widget.after(0, self.earned_widget.config, {"text": msg})

        # Update category breakdown
        self._update_category_widgets()

    def refresh_view_mode(self):
        """Refresh the view mode when preferences change"""
        log_debug("Refreshing view mode")
        # Update the entire display to handle preference changes properly
        self.update_display()

    def refresh_total_credits_visibility(self):
        """Refresh total credits visibility based on preference"""
        if hasattr(self, 'total_credits_label') and hasattr(self, 'total_credits_widget'):
            if self.preferences.cached_show_total_credits:
                # Only show if we're in full view mode
                if self.preferences.cached_view_mode == "full":
                    self.total_credits_label.grid()
                    self.total_credits_widget.grid()
                else:
                    self.total_credits_label.grid_remove()
                    self.total_credits_widget.grid_remove()
            else:
                # Always hide if preference is disabled
                self.total_credits_label.grid_remove()
                self.total_credits_widget.grid_remove()
