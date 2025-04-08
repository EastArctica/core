"""The WakaTime integration."""

from __future__ import annotations

from dataclasses import dataclass

from wakatime_api import ApiClient, Configuration
from wakatime_api.api.users_api import UsersApi
from wakatime_api.rest import ApiException

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import LOGGER

PLATFORMS: list[Platform] = [Platform.SENSOR]
type WakaTimeConfigEntry = ConfigEntry[WakaTimeData]


@dataclass
class WakaTimeData:
    """WakaTime data type."""

    client: ApiClient


async def async_setup_entry(hass: HomeAssistant, entry: WakaTimeConfigEntry) -> bool:
    """Set up WakaTime from a config entry."""

    configuration = Configuration()
    configuration.api_key["api_key"] = entry.data.get("api_key")

    if entry.data.get("api_key") is None:
        LOGGER.error("API key is missing")
        return False

    try:
        api_client = ApiClient(configuration)
    except ApiException as e:
        LOGGER.error("Error creating API client: %s", e)
        return False

    try:
        users_api = UsersApi(api_client)
        await hass.async_add_executor_job(users_api.get_current_user)
    except ApiException as e:
        if e.status == 401:
            LOGGER.error("Invalid API key: %s", e)
            return False
        if e.status == 403:
            LOGGER.error("API key is not authorized: %s", e)
            return False

        LOGGER.error("Error validating API connection: %s", e)
        return False

    entry.runtime_data = api_client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: WakaTimeConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
