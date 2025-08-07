"""
EDMC Income Tracker Plugin - Core income tracking logic
"""

import time
from config import config
from utils import CFG_EARNINGS, Transaction, log_debug, log_event

class EDMCIncome:
    """Main class for income tracking"""

    def __init__(self, ui_manager):
        self.ui = ui_manager
        self.saved_earnings = 0.0
        self.transactions = []

    def reset(self):
        """Reset all tracking data"""
        self.transactions = []
        self.saved_earnings = 0.0
        self.update_window()
        self.save()
        log_debug("Income Tracker reset")

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
        log_event("transaction", earnings, category)

    def register_docking(self):
        """Record a docking event"""
        data = Transaction(0.0, is_docking=True)
        self.transactions.append(data)
        self.update_window()
        self.save()

    def trip_earnings(self) -> float:
        """Calculate current trip earnings"""
        return sum(x.earnings for x in self.transactions)

    def trip_earnings_by_category(self, category: str) -> float:
        """Calculate current trip earnings for a specific category"""
        total = sum(x.earnings for x in self.transactions if x.category == category)
        log_debug(f"Category '{category}' earnings: {total:,.0f} Cr")
        return total

    def speed(self) -> float:
        """Calculate earning speed in Cr/hr"""
        earned = self.trip_earnings()
        if len(self.transactions) > 1:
            started = self.transactions[0].time
            now = time.time()
            if now > started:
                return earned * 3600.0 / (now - started)
        return 0.0

    def update_window(self):
        """Update the display widgets"""
        if self.ui:
            self.ui.update_display()

    def update_widget_visibility(self):
        """Update the visibility of category widgets based on Show settings"""
        if self.ui:
            self.ui.update_widget_visibility()

    def update_breakdown_visibility(self):
        """Update the visibility of the entire category breakdown section"""
        if self.ui:
            self.ui.update_breakdown_visibility()
