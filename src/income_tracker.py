"""
EDMC Income Tracker Plugin - Core income tracking logic
"""

import time
import json
from config import config # type: ignore
from src.constants import CFG_EARNINGS, CFG_SESSION_STATE
from src.utils import Transaction, log_debug, log_info, log_critical

class EDMCIncome:
    """Main class for income tracking"""

    def __init__(self, ui_manager):
        self.ui = ui_manager
        self.saved_earnings = 0.0
        self.transactions = []
        self.current_credits = 0

    def save_state(self):
        state = {
            "saved_earnings": self.saved_earnings,
            "transactions": [t.__dict__ for t in self.transactions],  # if Transaction is JSON-friendly
            "current_credits": self.current_credits,
        }
        config.set(CFG_SESSION_STATE, json.dumps(state))
        log_info("Income Tracker state saved")

    def load_state(self, reset_on_close=True):
        if reset_on_close:
            self.reset()
            return

        state_json = config.get_str(CFG_SESSION_STATE, default="")
        if not state_json:
            self.reset()
            log_info("Income Tracker state reset")
            return

        try:
            state = json.loads(state_json)
            self.saved_earnings = state.get("saved_earnings", 0.0)
            self.current_credits = state.get("current_credits", 0)
            self.transactions = [Transaction(**t) for t in state.get("transactions", [])]
            log_info(f"Income Tracker state restored ({len(self.transactions)} transactions)")
        except Exception as e:
            log_critical(f"Failed to load saved state: {e}")
            self.reset()


    def reset(self):
        """Reset all tracking data (current session + previous sessions)"""
        self.transactions = []
        self.saved_earnings = 0.0
        self.update_window()
        self.save()
        log_debug("Income Tracker reset: All data cleared")

    def load(self):
        """Load saved earnings from config"""
        saved = config.get_str(CFG_EARNINGS)
        if saved:
            try:
                self.saved_earnings = float(saved)
            except ValueError:
                self.saved_earnings = 0.0
        else:
            self.saved_earnings = 0.0

    def save(self):
        """Save current earnings to config"""
        total_earnings = self.saved_earnings + self.trip_earnings()
        config.set(CFG_EARNINGS, str(total_earnings))

    def transaction(self, earnings: float, category: str = "unknown"):
        """Record a transaction"""
        log_debug(f"Recording transaction: {earnings:,.0f} Cr ({category})")
        data = Transaction(earnings, category)
        self.transactions.append(data)
        log_debug(f"Total transactions: {len(self.transactions)}")
        self.update_window()
        self.save()
        log_debug(f"Transaction recorded: {earnings:,.0f} Cr ({category})")

    # Docking events are no longer needed - hourly rates are calculated
    # based on actual transaction timing, not docking events

    def trip_earnings(self) -> float:
        """Calculate current trip earnings"""
        return sum(x.earnings for x in self.transactions)

    def trip_earnings_by_category(self, category: str) -> float:
        """Calculate current trip earnings for a specific category"""
        total = sum(x.earnings for x in self.transactions if x.category == category)
        log_debug(f"Category '{category}' earnings: {total:,.0f} Cr")
        return total

    def speed(self) -> float:
        """Calculate earning speed based on actual play time, not wall clock time"""
        if not self.transactions:
            return 0.0

        total_earned = self.trip_earnings()
        total_play_time = 0.0

        for i in range(1, len(self.transactions)):
            # Calculate time between consecutive transactions
            time_diff = self.transactions[i].time - self.transactions[i-1].time

            # Only count as "play time" if transactions are close together
            # (e.g., max 30 minutes between transactions = active play)
            if time_diff < 1800:  # 30 minutes
                total_play_time += time_diff

        if total_play_time > 0:
            return (total_earned * 3600.0) / total_play_time

        # Fallback: if no play time calculated, use current session time
        if len(self.transactions) > 1:
            started = self.transactions[0].time
            now = time.time()
            if now > started:
                return total_earned * 3600.0 / (now - started)

        return 0.0

    def update_window(self):
        """Update the display widgets"""
        if self.ui:
            self.ui.update_display()

    def update_credits(self, credits: int):
        """Update current credit balance from journal state"""
        if self.current_credits != credits:
            log_debug(f"[CREDITS] Credits updated: {self.current_credits:,} -> {credits:,}")
            self.current_credits = credits
            self.update_window()

    def get_current_credits(self) -> int:
        """Get current credit balance"""
        return self.current_credits

    def refresh_ui(self):
        """Update the visibility of the entire category breakdown section"""
        log_debug("Refreshing UI")
        if self.ui:
            self.ui.refresh_ui()
