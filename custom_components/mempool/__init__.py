"""Mempool.space integration for Home Assistant."""

from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MempoolApiClient
from .const import CONF_BASE_URL
from .coordinator import MempoolDataUpdateCoordinator
from .data import MempoolConfigEntry, MempoolData

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: MempoolConfigEntry) -> bool:
    """Set up Mempool from a config entry."""
    session = async_get_clientsession(hass)
    client = MempoolApiClient(entry.data[CONF_BASE_URL], session)

    coordinator = MempoolDataUpdateCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = MempoolData(client=client, coordinator=coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: MempoolConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
