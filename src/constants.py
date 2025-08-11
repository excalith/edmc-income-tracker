"""
EDMC Income Tracker Plugin - Constants and configuration
"""

# Plugin information
PLUGIN_NAME = "EDMC Income Tracker"
PLUGIN_VERSION = "0.1.0"

# Log when constants are loaded
try:
    from .utils import log_debug
    log_debug(f"[VERSIONCODE] Constants loaded - Plugin: {PLUGIN_NAME}, Version: {PLUGIN_VERSION}")
except ImportError:
    # Fallback if utils not available yet
    pass

# URLs
GITHUB_REPO_URL = "https://github.com/excalith/edmc-income-tracker"
#GITHUB_API_URL = "https://api.github.com/repos/excalith/edmc-income-tracker/releases/latest"
GITHUB_API_URL = "https://api.github.com/repos/excalith/excalith-start-page/releases/latest" # TEST ONLY

# Configuration keys
CFG_EARNINGS = "EDMCIncome_earnings"
CFG_TRACK_TRADING = "EDMCIncome_track_trading"
CFG_TRACK_COMBAT = "EDMCIncome_track_combat"
CFG_TRACK_EXPLORATION = "EDMCIncome_track_exploration"
CFG_TRACK_MISSIONS = "EDMCIncome_track_missions"
CFG_RESET_ON_CLOSE = "EDMCIncome_reset_on_close"
