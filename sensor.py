import logging

from .const import (
    DOMAIN,
    CONF_CLIENT
)

from .steca_coordinator import StecaCoordinator

from .steca_sensor import StecaGridSensor

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
    SensorEntityDescription
)

from homeassistant.const import (PERCENTAGE, UnitOfElectricPotential, UnitOfPower, UnitOfElectricCurrent)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant,entry: ConfigEntry, async_add_entities: AddEntitiesCallback):

    data = hass.data[DOMAIN][entry.entry_id]

    steca = data[CONF_CLIENT]
    coordinator: StecaCoordinator = data["coordinator"]

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
