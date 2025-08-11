"""
EDMC Income Tracker Plugin - Journal entry processing
"""

from src.utils import log_debug
from src.constants import JOURNAL_EVENT_CATEGORIES, JOURNAL_FIELDS

class JournalProcessor:
    """Handles processing of Elite Dangerous journal entries"""

    def __init__(self, income_tracker, preferences_manager):
        self.income_tracker = income_tracker
        self.preferences = preferences_manager

    def process_journal_entry(self, cmdr, is_beta, system, station, entry, state):
        """Process a journal entry and update income tracking."""
        # Always handle credits state
        if 'Credits' in state:
            log_debug(f"[CREDITS] {state['Credits']:,}")
            self.income_tracker.update_credits(state['Credits'])

        if 'IsDocked' in state:
            log_debug(f"[STATE] IsDocked: {state['IsDocked']}")

        event = entry.get("event")
        if not event:
            return "No event found"

        prefs = self.preferences
        track_map = {
            "trading": prefs.cached_track_trading,
            "combat": prefs.cached_track_combat,
            "exploration": prefs.cached_track_exploration,
            "missions": prefs.cached_track_missions,
        }

        for category, events in JOURNAL_EVENT_CATEGORIES.items():
            if category != "maintenance" and not track_map.get(category, False):
                continue

            if event not in events:
                continue

            key_names, signs = events[event]
            amounts_found = False

            for key_name, sign in zip(key_names, signs):
                journal_key = JOURNAL_FIELDS.get(key_name)
                if not journal_key:
                    log_debug(f"Unknown field key: {key_name} in event {event}")
                    continue

                amount = entry.get(journal_key, 0)
                if amount:
                    self.income_tracker.transaction(sign * amount, category)
                    amounts_found = True

            if amounts_found:
                log_debug(f"Processed event `{event}` in category `{category}`")
                return f"Event: {event}"

        log_debug(f"Skipping unknown or untracked event: {event}")
        return None

    def process_dashboard_entry(self, cmdr, is_beta, entry):
        """No dashboard processing needed."""
        pass
