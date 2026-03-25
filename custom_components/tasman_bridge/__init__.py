"""The Tasman Bridge integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import DATA_THEMES
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .const import DOMAIN, DEFAULT_COLOR_HEX
from .coordinator import TasmanBridgeCoordinator

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Tasman Bridge from a config entry."""
    coordinator = TasmanBridgeCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def update_theme_and_state(*args):
        """Calculate the active color and update the HA Theme."""
        current_time = dt_util.now()
        events = coordinator.data or []
        
        active_hex = DEFAULT_COLOR_HEX
        for event in events:
            # Check if current time falls within the 12:00 PM to 12:00 PM window
            if event["active_start"] <= current_time < event["active_end"]:
                active_hex = event["color_hex"]
                break
        
        # Inject custom theme into Home Assistant
        if DATA_THEMES in hass.data:
            # Fixed: In modern HA versions, DATA_THEMES is a dictionary itself
            hass.data[DATA_THEMES]["Tasman Bridge"] = {
                "primary-color": active_hex,
                "accent-color": active_hex
            }
            hass.bus.async_fire("themes_updated")

    # Update theme immediately on boot and every time coordinator fetches
    coordinator.async_add_listener(update_theme_and_state)
    await update_theme_and_state()

    # Schedule targeted refresh times
    # 11:30 AM: Scrape latest data from government website
    async def fetch_latest(*args):
        await coordinator.async_request_refresh()
    async_track_time_change(hass, fetch_latest, hour=11, minute=30, second=0)

    # 12:00 PM: Force refresh to trigger the midday state & theme rollover
    async_track_time_change(hass, fetch_latest, hour=12, minute=0, second=1)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
