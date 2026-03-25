"""Constants for the Tasman Bridge integration."""
from datetime import timedelta

DOMAIN = "tasman_bridge"

SCRAPE_URL = "https://www.transport.tas.gov.au/road_permits/permits_and_bookings/tasman_bridge_lights"

# Update interval serves as a fallback. 
# We explicitly schedule targeted updates at 11:30 AM and 12:00 PM in __init__.py
UPDATE_INTERVAL = timedelta(hours=6)

# Map government text to Hex values
COLOR_MAP = {
    "violet": "#8A2BE2",
    "yellow": "#FFD700",
    "red": "#FF0000",
    "blue": "#0000FF",
    "cyan": "#00FFFF",
    "rose": "#FF007F",
    "orange": "#FFA500",
    "warm white": "#FDF4DC"
}

DEFAULT_COLOR = "warm white"
DEFAULT_COLOR_HEX = COLOR_MAP[DEFAULT_COLOR]
