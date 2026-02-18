"""Config flow for Mempool integration."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MempoolApiClient, MempoolApiConnectionError, MempoolApiError
from .const import CONF_BASE_URL, DEFAULT_BASE_URL, DOMAIN, LOGGER

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
    }
)


class MempoolFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Mempool."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].rstrip("/")

            # Derive unique ID from the URL hostname
            parsed = urlparse(base_url)
            unique_id = parsed.hostname or base_url
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            # Test connection
            session = async_get_clientsession(self.hass)
            client = MempoolApiClient(base_url, session)
            try:
                await client.async_get_backend_info()
            except MempoolApiConnectionError:
                errors["base"] = "cannot_connect"
            except MempoolApiError:
                errors["base"] = "cannot_connect"
            except Exception:
                LOGGER.exception("Unexpected error during config flow")
                errors["base"] = "unknown"

            if not errors:
                title = parsed.hostname or base_url
                return self.async_create_entry(
                    title=title,
                    data={CONF_BASE_URL: base_url},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
