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

        # Log all events to see what we're receiving
        if event not in ['FSDJump', 'Location', 'Docked', 'Undocked', 'SupercruiseEntry', 'SupercruiseExit']:
            log_debug(f"Event details: {event} - {entry}")

        # Check if state contains credit balance information
        if 'Credits' in state:
            log_debug(f"State contains credits: {state['Credits']:,.0f} Cr")

            # Update the UI with the actual balance from state
            if self.income_tracker.ui:
                self.income_tracker.ui.update_credits_from_state(state['Credits'])

        # Check if tracking is enabled for each category
        track_trading = self.preferences.cached_track_trading
        track_combat = self.preferences.cached_track_combat
        track_exploration = self.preferences.cached_track_exploration
        track_missions = self.preferences.cached_track_missions

        # Trading events
        if track_trading:
            if event == "MarketSell":
                self.income_tracker.transaction(entry["TotalSale"], "trading")
            elif event == "MarketBuy":
                self.income_tracker.transaction(-entry["TotalCost"], "trading")
            elif event == "BuyTradeData":
                self.income_tracker.transaction(-entry["Cost"], "trading")

        # Combat events
        if track_combat:
            if event == "RedeemVoucher":
                self.income_tracker.transaction(entry["Amount"], "combat")

        # Exploration events
        if track_exploration:
            if event == "SellExplorationData":
                self.income_tracker.transaction(entry["TotalEarnings"], "exploration")

        # Mission events
        if track_missions:
            if event == "MissionCompleted":
                if "Dontation" in entry:
                    self.income_tracker.transaction(-entry["Dontation"], "missions")
                else:
                    self.income_tracker.transaction(entry["Reward"], "missions")
            elif event == "CommunityGoalReward":
                self.income_tracker.transaction(entry["Reward"], "missions")

        # Credits events (always tracked)
        if event == "Credits":
            log_debug(f"Processing Credits event: {entry}")

            # Check if state contains the actual credit balance
            if 'Credits' in state:
                credits_balance = state['Credits']
                log_debug(f"Using state credits balance: {credits_balance:,.0f} Cr")

                # Update the UI with the actual balance from state
                if self.income_tracker.ui:
                    self.income_tracker.ui.update_credits_from_state(credits_balance)

                return f"Event: {event} - Balance: {credits_balance:,.0f} Cr"
            else:
                log_debug(f"Credits event but no state credits available: {entry}")
                return f"Event: {event} - No state data"

        # Docking events (always tracked for rate calculation)
        if event == "Docked":
            self.income_tracker.register_docking()

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
