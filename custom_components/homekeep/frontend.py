"""Frontend registration for the Homekeep sidebar app."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .const import DOMAIN, NAME

PANEL_URL_PATH = DOMAIN
PANEL_COMPONENT_NAME = "homekeep-panel"
PANEL_STATIC_URL = f"/{DOMAIN}_static/homekeep-panel.js"
PANEL_TITLE = NAME
PANEL_ICON = "mdi:home-heart"

_PANEL_JS_PATH = Path(__file__).with_name("frontend") / "homekeep-panel.js"


async def async_register_frontend(hass: Any) -> None:
    """Register the Homekeep non-iframe sidebar panel."""

    from homeassistant.components import frontend
    from homeassistant.components.http import StaticPathConfig

    await hass.http.async_register_static_paths(
        [StaticPathConfig(PANEL_STATIC_URL, str(_PANEL_JS_PATH), False)]
    )
    frontend.async_register_built_in_panel(
        hass,
        component_name="custom",
        sidebar_title=PANEL_TITLE,
        sidebar_icon=PANEL_ICON,
        frontend_url_path=PANEL_URL_PATH,
        config={
            "_panel_custom": {
                "name": PANEL_COMPONENT_NAME,
                "module_url": PANEL_STATIC_URL,
                "embed_iframe": False,
                "trust_external": False,
            },
            "mock_ready_now": True,
        },
        update=True,
    )


def async_unregister_frontend(hass: Any) -> None:
    """Remove the Homekeep sidebar panel."""

    from homeassistant.components import frontend

    frontend.async_remove_panel(hass, PANEL_URL_PATH, warn_if_unknown=False)
