from __future__ import annotations

import asyncio
import logging
import threading

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from .const import MODBUS_ADDRESS, MODBUS_SLAVE, DISCRETE_INPUT_COUNT, CONF_MODEL, bridgeModels

_LOGGER = logging.getLogger(__name__)

_MODBUS_TIMEOUT = 10


class ModbusNotEnabledError(Exception):
    """Raised when the device does not answer Modbus requests."""


class ModbusHub:
    """Manage the Modbus TCP connection to the Ebyte M31 device."""

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._lock = threading.Lock()
        self._client = ModbusTcpClient(host=host, port=port, timeout=_MODBUS_TIMEOUT)

    def _connect(self) -> None:
        if not self._client.connect():
            raise ConnectionError(f"Could not connect to {self._host}:{self._port}")

    async def async_validate_modbus_protocol(self) -> None:
        """Validate that the Modbus endpoint is reachable."""
        await asyncio.to_thread(self._connect)
        try:
            await asyncio.to_thread(self._read_discrete_inputs, MODBUS_ADDRESS, 1)
        except ModbusException as err:
            raise ModbusNotEnabledError(str(err)) from err

    async def async_read_discrete_inputs(self, count: int, address: int = MODBUS_ADDRESS) -> list[bool]:
        """Read discrete inputs from the configured Modbus address and slave."""
        await asyncio.to_thread(self._connect)
        with self._lock:
            result = self._client.read_discrete_inputs(
                address=address,
                count=count,
                device_id=MODBUS_SLAVE,
            )
            if result.isError():
                raise ModbusException(f"Error reading discrete inputs at {address}")
            return [bool(value) for value in result.bits]

    async def async_close(self) -> None:
        """Close the underlying client."""
        with self._lock:
            self._client.close()

    def _read_discrete_inputs(self, address: int, count: int) -> list[bool]:
        result = self._client.read_discrete_inputs(
            address=address,
            count=count,
            device_id=MODBUS_SLAVE,
        )
        if result.isError():
            raise ModbusException(f"Error reading discrete inputs at {address}")
        return [bool(value) for value in result.bits]
        
    def switch_set(self, address: int, state: int) -> None:
        await asyncio.to_thread(self._connect)
        with self._lock:
            self._client.write_coil(address=address, value=state, device_id=MODBUS_SLAVE)
