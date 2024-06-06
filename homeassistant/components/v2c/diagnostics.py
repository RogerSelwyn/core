"""Diagnostics support for V2C."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import V2CUpdateCoordinator

TO_REDACT = {CONF_HOST, "title"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: V2CUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    if TYPE_CHECKING:
        assert coordinator.evse

    coordinator_data = coordinator.evse.data
    evse_raw_data = coordinator.evse.raw_data

    return {
        "config_entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "data": str(coordinator_data),
        "raw_data": evse_raw_data["content"].decode("utf-8"),  # type: ignore[attr-defined]
        "host_status": evse_raw_data["status_code"],
    }
