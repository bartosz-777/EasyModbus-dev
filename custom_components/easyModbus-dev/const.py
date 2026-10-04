"""Constants for the EasyModbus integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.const import CONF_HOST, CONF_PORT

DOMAIN = "easyModbus-dev"

DEFAULT_HOST = ""
DEFAULT_PORT = 502

MODBUS_ADDRESS = 0
MODBUS_SLAVE = 1
DISCRETE_INPUT_COUNT = 8

CONF_MODEL = "Model"
CONF_INPUTS = "Inputs number"
CONF_OUTPUTS = "Outputs number"
CONF_FLIP_INPUTS = "Flip inputs"
CONF_FLIP_OUTPUTS = "Flip outputs"
CONF_FLIP_INPUTS_MASK = "Bitmask: set 1 to apply input Flip; 0 to leave unchanged; has to be length of inputs number"

@dataclass(frozen=True)
class BinarySensorDefinition:
    """Definition for one discrete input entity."""

    key: str
    name: str
    address: int
    icon: str | None = None


BINARY_SENSOR_DEFINITIONS: tuple[BinarySensorDefinition, ...] = tuple(
    BinarySensorDefinition(
        key=f"input_{index}",
        name=f"Discrete input {index}",
        address=index,
        icon="mdi:toggle-switch",
    )
    for index in range(DISCRETE_INPUT_COUNT)
)

bridgeModels = {
    "AAAX4440G": {"name": "AAAX4440G", "digital_inputs": 4, "digital_outputs": 4, "analog_inputs": 4, "analog_outputs": 0},
    "AXAX4040G": {"name": "AXAX4040G", "digital_inputs": 4, "digital_outputs": 4, "analog_inputs": 4, "analog_outputs": 0},
    "AXAX8080G": {"name": "AXAX8080G", "digital_inputs": 8, "digital_outputs": 8, "analog_inputs": 8, "analog_outputs": 0},
    "AXXX8000G": {"name": "AXXX8000G", "digital_inputs": 8, "digital_outputs": 8, "analog_inputs": 8, "analog_outputs": 0},
    "XXAX0080G": {"name": "XXAX0080G", "digital_inputs": 0, "digital_outputs": 8, "analog_inputs": 8, "analog_outputs": 0},
    "AXXXA000G": {"name": "AXXXA000G", "digital_inputs": 16, "digital_outputs": 0, "analog_inputs": 0, "analog_outputs": 0},
    "XXAX00AOG": {"name": "XXAX00AOG", "digital_inputs": 0, "digital_outputs": 16, "analog_inputs": 0, "analog_outputs": 0},
    "XAXX0800G": {"name": "XAXX0800G", "digital_inputs": 0, "digital_outputs": 0, "analog_inputs": 8, "analog_outputs": 0},
    "XAXA0404G": {"name": "XAXA0404G", "digital_inputs": 0, "digital_outputs": 0, "analog_inputs": 4, "analog_outputs": 0},
    "XXXA0008G": {"name": "XXXA0008G", "digital_inputs": 0, "digital_outputs": 0, "analog_inputs": 0, "analog_outputs": 8},
    "XFXX0800G": {"name": "XFXX0800G", "digital_inputs": 0, "digital_outputs": 0, "analog_inputs": 8, "analog_outputs": 0},
    "XGXX0800G": {"name": "XGXX0800G", "digital_inputs": 0, "digital_outputs": 0, "analog_inputs": 8, "analog_outputs": 0}
}
def get_binary_sensor_definitions(input_count: int) -> tuple[BinarySensorDefinition, ...]:
    """Generate definitions for discrete input entities dynamically."""
    return tuple(
        BinarySensorDefinition(
            key=f"input_{index}",
            name=f"Discrete input {index}",
            address=index,
            icon="mdi:toggle-switch",
        )
        for index in range(input_count)
    )
def get_switch_definitions(outputs_count: int) -> tuple[BinarySensorDefinition, ...]:
    "Create definitions for outputs(switches)"
    return tuple(
        BinarySensorDefinition(
            key=f"output_{index}",
            name=f"Relay {index}",
            address=index,
            icon="mdi:toggle-switch",
        )
        for index in range(outputs_count)
    )
