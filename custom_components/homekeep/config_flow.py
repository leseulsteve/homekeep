"""Config flow for Homekeep."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import DOMAIN, NAME
from .calendar_context import OPTION_CALENDAR_ENTITY_IDS


class HomekeepConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Homekeep."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Create the Homekeep config entry."""

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title=NAME, data={})

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""

        return HomekeepOptionsFlow()


class HomekeepOptionsFlow(config_entries.OptionsFlow):
    """Handle Homekeep options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Manage Homekeep options."""

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self._options_schema(),
        )

    def _options_schema(self) -> Any:
        """Return the Homekeep options schema."""

        import voluptuous as vol

        return vol.Schema(
            {
                vol.Optional(
                    OPTION_CALENDAR_ENTITY_IDS,
                    default=[],
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="calendar",
                        multiple=True,
                    )
                ),
            }
        )
