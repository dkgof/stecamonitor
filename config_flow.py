from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_IP, CONF_UPDATE_INTERVAL
from .StecaAPI import StecaAPI

_LOGGER = logging.getLogger(__name__)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]):
    """Validate input during setup."""
    ip = data[CONF_IP]

    api = StecaAPI(hass, ip)

    # Try one quick poll to validate the connection
    result = await hass.async_add_executor_job(api.poll)
    if result is None:
        raise ConnectionError("No data returned from inverter")

    return data

class StecaGridConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for StecaGrid Monitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception as ex:
                _LOGGER.exception("Unexpected error: %s", ex)
                errors["base"] = "unknown"
            else:
                # Prevent duplicates
                await self.async_set_unique_id(info[CONF_IP])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"StecaGrid {info[CONF_IP]}",
                    data=info,
                )

        data_schema = vol.Schema({
            vol.Required(CONF_IP): str,
            vol.Optional(CONF_UPDATE_INTERVAL, default=5): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

    async def async_step_import(self, user_input=None) -> FlowResult:
        """Handle YAML import."""

        await self.async_set_unique_id(user_input[CONF_IP])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"StecaGrid {user_input[CONF_IP]}",
            data=user_input,
        )
