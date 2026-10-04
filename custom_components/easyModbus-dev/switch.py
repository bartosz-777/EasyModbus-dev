from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

##from .const import get_binary_sensor_definitions, DOMAIN, BinarySensorDefinition
from .const import *
from .coordinator import EbyteM31Coordinator
from .entity import EbyteM31Entity
from .hub import *

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: EbyteM31Coordinator = hass.data[DOMAIN][entry.entry_id]["standard"]
    hub: ModbusHub = hass.data[DOMAIN][entry.entry_id]["hub"]
    config = {**entry.data, **entry.options}
    outputs = config[CONF_OUTPUTS]
    switch_defs = get_switch_definitions(outputs)
    async_add_entities(
        ModbusSwitch(coordinator,hub, entry , defn)
        for defn in switch_defs
    )


class ModbusSwitch(EbyteM31Entity, SwitchEntity):
    def __init__(
        self,
        coordinator: EbyteM31Coordinator,
        hub: ModbusHub,
        entry: ConfigEntry,
        defn: BinarySensorDefinition,
    ) -> None:
        super().__init__(coordinator, entry.entry_id , defn.key, defn.name)
        self._defn = defn
        if defn.icon:
            self._attr_icon = defn.icon
        self._is_on = False
        self.hub = hub
        self._config = {**entry.data, **entry.options}

    @property
    def is_on(self) -> bool | None:
        """Return true if switch is on."""
        return self._is_on

    def turn_on(self, **kwargs: Any):
        """Turn the switch on."""
        self._is_on = True
        self.hub.switch_set(self._defn.address, 0 if self._config[CONF_FLIP_OUTPUTS] else 1)

    def turn_off(self, **kwargs: Any):
        """Turn the switch off."""
        self._is_on = False
        self.hub.switch_set(self._defn.address, 1 if self._config[CONF_FLIP_OUTPUTS] else 0)
