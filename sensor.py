import logging

import sys
import async_timeout

from .const import (
    DOMAIN,
    CONF_CLIENT,
    CONF_IP,
    CONF_PLATFORM,
    CONF_UPDATE_INTERVAL
)

from homeassistant.core import callback

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    SensorEntityDescription
)

from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.const import (PERCENTAGE, UnitOfElectricPotential, UnitOfPower, UnitOfElectricCurrent)

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):

    steca = hass.data[DOMAIN][CONF_CLIENT]
    update_interval = hass.data[DOMAIN][CONF_UPDATE_INTERVAL]

    coordinator = StecaCoordinator(hass, steca, update_interval)

    await coordinator.async_config_entry_first_refresh()

    entities = [
        StecaGridSensor(coordinator, steca, SensorEntityDescription(
            key="acpower",
            name="AC Power",
            native_unit_of_measurement=UnitOfPower.WATT,
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
        )),
        StecaGridSensor(coordinator, steca, SensorEntityDescription(
            key="acvoltage",
            name="AC Voltage",
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
        )),
        StecaGridSensor(coordinator, steca, SensorEntityDescription(
            key="accurrent",
            name="AC Current",
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
        )),
        StecaGridSensor(coordinator, steca, SensorEntityDescription(
            key="dcvoltage",
            name="DC Voltage",
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
        )),
        StecaGridSensor(coordinator, steca, SensorEntityDescription(
            key="dccurrent",
            name="DC Current",
            native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
        )),
        StecaGridSensor(coordinator, steca, SensorEntityDescription(
            key="derating",
            name="Derating",
            native_unit_of_measurement=PERCENTAGE,
            device_class=None,
            state_class=SensorStateClass.MEASUREMENT,
        ))
    ]

    async_add_entities(entities)

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

class StecaGridSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, steca, description):
        super().__init__(coordinator)

        self.entity_description = description

        self._attr_name = f"Steca Inverter {steca.getIp()} {description.name}"
        self._attr_unique_id = f"steca_inverter_{steca.getSerial()}_{description.key}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""

        self._attr_native_value = self.coordinator.data[self.entity_description.key]
        self.async_write_ha_state()

    @property
    def should_poll(self):
        return False