"""Config flow for the Ebyte M31 integration."""
from __future__ import annotations

import logging
from typing import Any, override

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import callback
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_HOST, DEFAULT_PORT, DOMAIN, bridgeModels, CONF_MODEL, CONF_INPUTS, CONF_OUTPUTS, CONF_FLIP_INPUTS, CONF_FLIP_OUTPUTS, CONF_FLIP_INPUTS_BITMASK
from .hub import ModbusHub, ModbusNotEnabledError

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_INPUTS, default=8): int,
        vol.Required(CONF_OUTPUTS, default=8): int,
        vol.Required(CONF_FLIP_INPUTS, default=False): bool,
        vol.Required(CONF_FLIP_INPUTS_BITMASK, default=11111111): vol.All(str, vol.Contains([0,1])),
        vol.Required(CONF_FLIP_OUTPUTS, default=False): bool,
    }
)

class ModbusBinaryConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1
    DOMAIN = DOMAIN
    @override
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
     errors = {}
     if user_input:
        ip_address = user_input[CONF_HOST]
        port = user_input[CONF_PORT]
        #CONF_FLIP_INPUTS = user_input[CONF_FLIP_INPUTS]
        #CONF_FLIP_OUTPUTS = user_input[CONF_FLIP_OUTPUTS]
        hub = None
        try:
            hub = ModbusHub(ip_address, port)
            await hub.async_validate_modbus_protocol()
            await self.async_set_unique_id(ip_address)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="EasyModbus", data=user_input)
        except (ConnectionError, ModbusNotEnabledError):
            errors["base"] = "cannot_connect"
        finally:
            if hub is not None:
                await hub.async_close()
     return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors,)
