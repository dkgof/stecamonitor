#The StecaGrid Monitor integration.
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import async_load_platform
from .StecaAPI import StecaAPI

from .const import (
    DOMAIN,
    CONF_CLIENT,
    CONF_IP,
    CONF_PLATFORM,
    CONF_UPDATE_INTERVAL
)


PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    conf = config.get(DOMAIN)

    if conf is None:
        return True

    ip = conf.get(CONF_IP, "")
    update_interval = conf.get(CONF_UPDATE_INTERVAL, 5)

    steca = StecaAPI(hass, ip)

    hass.data[DOMAIN] = {CONF_CLIENT: steca, CONF_UPDATE_INTERVAL: update_interval}

    # Add sensors
    hass.async_create_task(
        async_load_platform(hass, CONF_PLATFORM, DOMAIN, conf, config)
    )

    return True
