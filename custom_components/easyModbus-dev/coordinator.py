"""Data coordinator for the Ebyte M31 Modbus integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, bridgeModels, CONF_MODEL, CONF_INPUTS, CONF_OUTPUTS, CONF_FLIP_INPUTS, CONF_FLIP_OUTPUTS, CONF_FLIP_INPUTS_MASK

if TYPE_CHECKING:
    from .hub import ModbusHub

_LOGGER = logging.getLogger(__name__)


class EbyteM31Coordinator(DataUpdateCoordinator[dict[str, bool]]):
    """Coordinate polling of the discrete input register values."""

    def __init__(self, hass: HomeAssistant, hub: ModbusHub,inputs: int,outputs: int,flipInputs: bool, flipOutputs: bool,flipInputsMask: int) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=10),
        )
        self.hub = hub
        self.inputs = inputs
        self.flipInputs = flipInputs
        self.flipInputsMask = [bool(flipInputsMask & (1 << i)) for i in range(self.inputs - 1, -1, -1)]
    async def _async_update_data(self) -> dict[str, bool]:
        values = await self.hub.async_read_discrete_inputs(count=self.inputs)
        if self.flipInputs:
            return {f"input_{index}": bool(not value if self.flipInputsMask[index] else value) for index, value in enumerate(values)}
        else:
            return {f"input_{index}": bool(value) for index, value in enumerate(values)}
#bridgeModels[CONF_MODEL]["digital_inputs"]
