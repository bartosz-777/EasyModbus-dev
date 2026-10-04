"""Base entity for the Ebyte M31 integration."""
from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from .coordinator import EbyteM31Coordinator
from .const import DOMAIN, CONF_PORT, CONF_HOST


class EbyteM31Entity(CoordinatorEntity[EbyteM31Coordinator]):
    """Common entity behavior for the integration."""
    
    _attr_has_entity_name = True

    def __init__(self, coordinator: EbyteM31Coordinator, entry_id: str, key: str, name: str) -> None:
        super().__init__(coordinator)
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{key}"
        self._key = key
        self._attr_device_info = DeviceInfo(
            name= f"Modbus device",
            identifiers={(DOMAIN, entry_id) },
            model="v0.1",
            manufacturer="Ebyte",
        )

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_update(self) -> None:
        await self.coordinator.async_request_refresh()
