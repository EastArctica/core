"""Config flow for the WakaTime integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from wakatime_api import ApiClient, Configuration
from wakatime_api.api.users_api import UsersApi
from wakatime_api.rest import ApiException

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY

from .const import DOMAIN


class WakaTimeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WakaTime."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            configuration = Configuration()
            configuration.api_key["api_key"] = user_input[CONF_API_KEY]
            client = ApiClient(configuration)

            try:
                users_api = UsersApi(client)
                user = users_api.get_current_user()
            except ApiException as e:
                if e.status == 401:
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user.data.id)
                self._abort_if_unique_id_configured(updates=user_input)
                return self.async_create_entry(
                    title=f"{user.data.username} [{user.data.id}]", data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the reconfiguration step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            configuration = Configuration()
            configuration.api_key["api_key"] = user_input[CONF_API_KEY]
            client = ApiClient(configuration)

            try:
                users_api = UsersApi(client)
                user = users_api.get_current_user()
            except ApiException as e:
                if e.status == 401:
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user.data.id)
                self._abort_if_unique_id_mismatch()
                return self.async_update_reload_and_abort(
                    self._get_reconfigure_entry(),
                    data_updates=user_input,
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                }
            ),
            errors=errors,
        )
