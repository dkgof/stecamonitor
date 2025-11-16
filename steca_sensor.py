from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription
)

from .steca_coordinator import StecaCoordinator

from homeassistant.core import callback

class StecaGridSensor(SensorEntity):
    def __init__(self, coordinator: StecaCoordinator, steca, description: SensorEntityDescription):
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_name = f"Steca Inverter {steca.getIp()} {description.name}"
        self._attr_unique_id = f"steca_inverter_{steca.getSerial()}_{description.key}"

    @property
    def native_value(self):
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )

    @callback
    def _handle_coordinator_update(self):
        self.async_write_ha_state()