"""Ebyte M31 Modbus integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant

from .const import CONF_MODEL, DOMAIN, CONF_FLIP_INPUTS, CONF_FLIP_OUTPUTS, CONF_INPUTS, CONF_OUTPUTS, CONF_FLIP_INPUTS_MASK
from .coordinator import EbyteM31Coordinator
from .hub import ModbusHub

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SWITCH, ]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Ebyte M31 integration."""
    config = {**entry.data, **entry.options}
    host = config[CONF_HOST]
    port = config[CONF_PORT]
    hub = ModbusHub(host, port)
    coordinator = EbyteM31Coordinator(hass, hub,config[CONF_INPUTS],config[CONF_OUTPUTS],config[CONF_FLIP_INPUTS],config[CONF_FLIP_OUTPUTS],config[CONF_FLIP_INPUTS_MASK])

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "hub": hub,
        "standard": coordinator,
        "host": host,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the integration."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    data = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    if data:
        await data["hub"].async_close()
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
