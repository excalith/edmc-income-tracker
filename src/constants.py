"""
EDMC Income Tracker Plugin - Constants and configuration
"""

# Plugin information
PLUGIN_NAME = "Income Tracker"
PLUGIN_VERSION = "0.1.0"

# URLs
GITHUB_REPO_URL = "https://github.com/excalith/edmc-income-tracker"
GITHUB_API_URL = "https://api.github.com/repos/excalith/edmc-income-tracker/releases/latest"
#GITHUB_API_URL = "https://api.github.com/repos/excalith/excalith-start-page/releases/latest" #TEST URL WITH RELEASES

# Configuration keys
CFG_EARNINGS = "EDMCIncome_earnings"
CFG_RESET_ON_CLOSE = "EDMCIncome_reset_on_close"
CFG_SHOW_TOTAL_CREDITS = "EDMCIncome_show_total_credits"
CFG_TRACK_TRADING = "EDMCIncome_track_trading"
CFG_TRACK_COMBAT = "EDMCIncome_track_combat"
CFG_TRACK_EXPLORATION = "EDMCIncome_track_exploration"
CFG_TRACK_MISSIONS = "EDMCIncome_track_missions"

# UI Element States - defines visibility rules for each element
UI_ELEMENT_STATES = {
    "title": {"always_show": True},
    "reset": {"always_show": True},
    "speed": {"show_in": ["full", "compact"]},
    "earned": {"show_in": ["full", "compact"]},
    "maintenance": {"show_in": ["full"]},
    "total_credits": {"show_in": ["full"], "enabled": "show_total_credits"},
    "breakdown_toggle": {"show_in": ["full"]},
	"trading": {"show_in": ["full"], "enabled": "track_trading", "requires": "show_breakdown"},
	"combat": {"show_in": ["full"], "enabled": "track_combat", "requires": "show_breakdown"},
	"exploration": {"show_in": ["full"], "enabled": "track_exploration", "requires": "show_breakdown"},
	"missions": {"show_in": ["full"], "enabled": "track_missions", "requires": "show_breakdown"},
}
