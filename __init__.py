#The StecaGrid Monitor integration.
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_CLIENT,
    CONF_IP,
    CONF_UPDATE_INTERVAL
)

from .StecaAPI import StecaAPI
from .steca_coordinator import StecaCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Handle YAML config and import it as config entries."""
    yaml_conf = config.get(DOMAIN)
    if yaml_conf is None:
        return True

    ip = yaml_conf[CONF_IP]
    update_interval = yaml_conf.get(CONF_UPDATE_INTERVAL, 5)

    # Prepare config entry data
    import_data = {
        CONF_IP: ip,
        CONF_UPDATE_INTERVAL: update_interval,
    }

    # Start import flow
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": "import"},
            data=import_data,
        )
    )

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up StecaGrid from a config entry."""

    ip = entry.data.get(CONF_IP, "")
    update_interval = entry.data.get(CONF_UPDATE_INTERVAL, 5)

    steca = StecaAPI(hass, ip)

    coordinator = StecaCoordinator(hass, steca, update_interval)

    # ⬅ IMPORTANT: first refresh BEFORE platform forwarding
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        CONF_CLIENT: steca,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
