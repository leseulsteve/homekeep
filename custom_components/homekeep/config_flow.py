"""Config flow for Homekeep."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import DOMAIN, NAME, OPTION_DEV_MODE
from .calendar_context import OPTION_CALENDAR_ENTITY_IDS


DEFAULT_DEV_MODE = True


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
            return self.async_create_entry(
                title=NAME,
                data={
                    OPTION_DEV_MODE: user_input.get(
                        OPTION_DEV_MODE, DEFAULT_DEV_MODE
                    ),
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_config_schema(),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""

        return HomekeepOptionsFlow()


class HomekeepOptionsFlow(config_entries.OptionsFlowWithReload):
    """Handle Homekeep options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Manage Homekeep options."""

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                self._options_schema(),
                self._suggested_options(),
            ),
        )

    def _options_schema(self) -> Any:
        """Return the Homekeep options schema."""

        import voluptuous as vol

        return vol.Schema(
            {
                vol.Optional(OPTION_DEV_MODE): selector.BooleanSelector(),
                vol.Optional(
                    OPTION_CALENDAR_ENTITY_IDS,
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="calendar",
                        multiple=True,
                    )
                ),
            }
        )

    def _suggested_options(self) -> dict[str, Any]:
        """Return suggested option values from entry options and setup data."""

        return {
            OPTION_DEV_MODE: _entry_option(
                self.config_entry, OPTION_DEV_MODE, DEFAULT_DEV_MODE
            ),
            OPTION_CALENDAR_ENTITY_IDS: _entry_option(
                self.config_entry, OPTION_CALENDAR_ENTITY_IDS, []
            ),
        }


def _config_schema() -> Any:
    """Return the initial Homekeep config schema."""

    import voluptuous as vol

    return vol.Schema(
        {
            vol.Optional(
                OPTION_DEV_MODE,
                default=DEFAULT_DEV_MODE,
            ): selector.BooleanSelector(),
        }
    )


def _entry_option(entry: Any, key: str, default: Any) -> Any:
    """Read an option with config data fallback for initial setup values."""

    options = getattr(entry, "options", {}) or {}
    if key in options:
        return options[key]
    data = getattr(entry, "data", {}) or {}
    return data.get(key, default)
