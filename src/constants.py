"""
EDMC Income Tracker Plugin - Constants and configuration
"""

# Plugin information
PLUGIN_NAME = "Income Tracker"
PLUGIN_VERSION = "0.1.0"

# Debug settings
DEBUG_MODE = False

# URLs
GITHUB_REPO_URL = "https://github.com/excalith/edmc-income-tracker"
GITHUB_API_URL = "https://api.github.com/repos/excalith/edmc-income-tracker/releases/latest"
#GITHUB_API_URL = "https://api.github.com/repos/excalith/excalith-start-page/releases/latest" #TEST URL WITH RELEASES

# Configuration Keys
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

# Event to category mappings for journal processing
# Journal Entry Fields
JOURNAL_FIELDS = {
    "total_sale":     "TotalSale",
    "total_cost":     "TotalCost",
    "cost":           "Cost",
    "amount":         "Amount",
    "total_earnings": "TotalEarnings",
    "reward":         "Reward",
    "donation":       "Donation",
    "fine":           "Fine",
    "price":          "Price",
}

# Journal Entry Event Mappings
JOURNAL_EVENT_CATEGORIES = {
    "trading": {
        "MarketSell":    (["total_sale"], [1]),
        "MarketBuy":     (["total_cost"], [-1]),
        "BuyTradeData":  (["cost"], [-1]),
        "SellMicroResources": (["price"], [1]),
    },
    "combat": {
        "RedeemVoucher":    (["amount"], [1]),
        "FactionKillBond":  (["reward"], [1]),
        "PayBounties":      (["amount"], [-1]),
        "PayFines":         (["amount"], [-1]),
    },
    "exploration": {
        "SellExplorationData":       (["total_earnings"], [1]),
        "MultiSellExplorationData":  (["total_earnings"], [1]),
        "BuyExplorationData":        (["cost"], [-1]),
    },
    "missions": {
        "MissionCompleted":     (["donation", "reward"], [-1, 1]),
        "MissionFailed":        (["fine"], [-1]),
        "MissionAbandoned":    (["fine"], [-1]),
        "CommunityGoalReward":  (["reward"], [1]),
    },
    "maintenance": {
        "RefuelAll":      (["cost"], [-1]),
        "RefuelPartial":  (["cost"], [-1]),
        "Repair":         (["cost"], [-1]),
        "RepairAll":      (["cost"], [-1]),
        "BuyAmmo":        (["cost"], [-1]),
        "BuyDrones":      (["total_cost"], [-1]),
        "SellDrones":     (["total_sale"], [1]),
        "RestockVehicle": (["cost"], [-1]),
        "Resurrect":      (["cost"], [-1]),
    },
}
