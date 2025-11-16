import logging
import sys
import async_timeout
from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

class StecaCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, steca, interval):
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="StecaGrid Inverter",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=interval),
        )
        self.steca = steca

    async def _async_update_data(self):
        for x in range(5):
            _LOGGER.info("Attempting to poll stecagrid %i / 5", (x+1))
            try:
                # Note: asyncio.TimeoutError and aiohttp.ClientError are already
                # handled by the data update coordinator.
                async with async_timeout.timeout(10):
                    return await self.hass.async_add_executor_job(self.steca.poll)
            except:
                _LOGGER.error("Error talking to StecaGrid inverter: %s", sys.exc_info())

        raise UpdateFailed("Failed 5 retries talking to StecaGrid inverter")
