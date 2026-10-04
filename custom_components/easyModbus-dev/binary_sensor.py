"""Binary sensor platform for the Ebyte M31 integration."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import get_binary_sensor_definitions, DOMAIN, BinarySensorDefinition
from .coordinator import EbyteM31Coordinator
from .entity import EbyteM31Entity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: EbyteM31Coordinator = hass.data[DOMAIN][entry.entry_id]["standard"]
    config = {**entry.data, **entry.options}
    inputs = config["Inputs number"]
    sensor_defs = get_binary_sensor_definitions(inputs)
    async_add_entities(
        EbyteM31BinarySensor(coordinator, entry.entry_id, defn)
        for defn in sensor_defs
    )


class EbyteM31BinarySensor(EbyteM31Entity, BinarySensorEntity):
    """A single discrete input exposed as a binary sensor."""

    def __init__(
        self,
        coordinator: EbyteM31Coordinator,
        entry_id: str,
        defn: BinarySensorDefinition,
    ) -> None:
        super().__init__(coordinator, entry_id, defn.key, defn.name)
        self._defn = defn
        if defn.icon:
            self._attr_icon = defn.icon

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._defn.key)
