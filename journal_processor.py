"""
EDMC Income Tracker Plugin - Journal entry processing
"""

from utils import log_debug

class JournalProcessor:
    """Handles processing of Elite Dangerous journal entries"""

    def __init__(self, income_tracker, preferences_manager):
        self.income_tracker = income_tracker
        self.preferences = preferences_manager

    def process_journal_entry(self, cmdr: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> str:
        """
        Process a journal entry and update income tracking

        Args:
            cmdr: Commander name
            is_beta: Whether this is a beta game
            system: Current system
            station: Current station
            entry: Journal entry data
            state: The current game state

        Returns:
            String description of the event processed
        """
        if "event" not in entry:
            return "No event found"

        event = entry["event"]

        # Check if tracking is enabled for each category
        track_trading = self.preferences.cached_track_trading
        track_combat = self.preferences.cached_track_combat
        track_exploration = self.preferences.cached_track_exploration
        track_missions = self.preferences.cached_track_missions

        # Debug logging for tracking settings
        log_debug(f"Tracking settings - Trading: {track_trading}, Combat: {track_combat}, Exploration: {track_exploration}, Missions: {track_missions}, Maintenance: Always enabled")

        #region Trading events
        if track_trading:
            if event == "MarketSell":
                self.income_tracker.transaction(entry["TotalSale"], "trading")
            elif event == "MarketBuy":
                self.income_tracker.transaction(-entry["TotalCost"], "trading")
            elif event == "BuyTradeData":
                self.income_tracker.transaction(-entry["Cost"], "trading")
        #endregion

        #region Combat events
        if track_combat:
            if event == "RedeemVoucher":
                self.income_tracker.transaction(entry["Amount"], "combat")
        #endregion

        #region Exploration events
        if track_exploration:
            if event == "SellExplorationData":
                log_debug(f"Processing SellExplorationData event: {entry}")
                if "TotalEarnings" in entry:
                    log_debug(f"Processing SellExplorationData (TotalEarnings): {entry['TotalEarnings']:,.0f} Cr")
                    self.income_tracker.transaction(entry["TotalEarnings"], "exploration")
            elif event == "BuyExplorationData":
                log_debug(f"Processing BuyExplorationData: {entry['Cost']:,.0f} Cr")
                self.income_tracker.transaction(-entry["Cost"], "exploration")
        #endregion

        #region Mission events
        if track_missions:
            if event == "MissionCompleted":
                if "Dontation" in entry:
                    self.income_tracker.transaction(-entry["Dontation"], "missions")
                else:
                    self.income_tracker.transaction(entry["Reward"], "missions")
            elif event == "CommunityGoalReward":
                self.income_tracker.transaction(entry["Reward"], "missions")
        #endregion

        #region Maintenance events (always tracked)
        if event == "RefuelAll":
            self.income_tracker.transaction(-entry["Cost"], "maintenance")
        elif event == "RefuelPartial":
            self.income_tracker.transaction(-entry["Cost"], "maintenance")
        elif event == "Repair":
            self.income_tracker.transaction(-entry["Cost"], "maintenance")
        elif event == "RepairAll":
            self.income_tracker.transaction(-entry["Cost"], "maintenance")
        elif event == "BuyAmmo":
            self.income_tracker.transaction(-entry["Cost"], "maintenance")
        elif event == "BuyDrones":
            self.income_tracker.transaction(-entry["TotalCost"], "maintenance")
        elif event == "SellDrones":
            self.income_tracker.transaction(-entry["TotalSale"], "maintenance")
        elif event == "RestockVehicle":
            self.income_tracker.transaction(-entry["Cost"], "maintenance")
        elif event == "Resurrect":
            self.income_tracker.transaction(-entry["Cost"], "maintenance")
        #endregion

        # Docking events are no longer needed for rate calculation
        # (Hourly rates are now calculated based on actual transaction timing)

        # Log certain events for debugging
        if event in ['MarketSell', 'MarketBuy', 'MissionCompleted', 'RedeemVoucher', 'SellExplorationData', 'Credits']:
            log_debug(f"Income Tracker detected {event} event")
            return f"Event: {event}"

        return None

    def process_dashboard_entry(self, cmdr: str, is_beta: bool, entry: dict) -> None:
        """
        Process a status.json entry (dashboard data).

        Args:
            cmdr: The current commander name
            is_beta: Whether running in beta mode
            entry: The status.json entry as a dictionary
        """
        # This basic plugin doesn't need to process dashboard entries
        pass
