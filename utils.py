"""
EDMC Income Tracker Plugin - Utility functions and constants
"""

import logging
import os
import sys
import time

# Debug settings
DEBUG_MODE = False


# Plugin information
plugin_name = os.path.basename(os.path.dirname(__file__))

# Set up logging
logger = logging.getLogger(f'{plugin_name}.{__name__}')

# Configuration keys
CFG_EARNINGS = "EDMCIncome_earnings"
CFG_TRACK_TRADING = "EDMCIncome_track_trading"
CFG_TRACK_COMBAT = "EDMCIncome_track_combat"
CFG_TRACK_EXPLORATION = "EDMCIncome_track_exploration"
CFG_TRACK_MISSIONS = "EDMCIncome_track_missions"
CFG_SHOW_TRADING = "EDMCIncome_show_trading"
CFG_SHOW_COMBAT = "EDMCIncome_show_combat"
CFG_SHOW_EXPLORATION = "EDMCIncome_show_exploration"
CFG_SHOW_MISSIONS = "EDMCIncome_show_missions"
CFG_RESET_ON_CLOSE = "EDMCIncome_reset_on_close"

# Module globals
this = sys.modules[__name__]

class Transaction:
    """Represents a transaction"""
    def __init__(self, earnings: float, category: str = "unknown", is_docking: bool = False):
        self.earnings = earnings
        self.category = category
        self.time = time.time()
        self.is_docking_event = 1.0 if is_docking else 0.0

def get_config_bool(config, key: str, default: bool = True) -> bool:
    """Get boolean config value with fallback"""
    if config.get_int(key) is not None:
        return bool(config.getint(key))
    return default

def log_event(event_name: str, earnings: float, category: str) -> None:
    """Log a transaction event"""
    logger.debug(f"Income Tracker: Transaction recorded: {earnings:,.0f} Cr ({category})")

def log_debug(message: str) -> None:
    """Log debug message"""
    logger.debug(message)

def log_warning(message: str) -> None:
    """Log warning message"""
    logger.warning(message)
