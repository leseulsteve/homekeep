"""The Homekeep integration."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    ATTR_AREA_ID,
    ATTR_ENTITY_ID,
    ATTR_FORCE,
    ATTR_REASON,
    ATTR_RECOMMENDATION_ID,
    DOMAIN,
    PLATFORMS,
    SERVICE_DISMISS_RECOMMENDATION,
    SERVICE_REFRESH_RECOMMENDATIONS,
)
from .store import HomekeepStorage

_LOGGER = logging.getLogger(__name__)


def _entry_stores(hass: HomeAssistant) -> dict[str, HomekeepStorage]:
    """Return Homekeep entry storage instances."""
    return hass.data.setdefault(DOMAIN, {})


def _first_store(hass: HomeAssistant) -> HomekeepStorage:
    """Return the first loaded Homekeep store for service handlers."""
    stores = hass.data.get(DOMAIN, {})
    if not stores:
        raise ServiceValidationError("Homekeep is not loaded")
    return next(iter(stores.values()))


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Homekeep services."""

    async def handle_refresh_recommendations(call: ServiceCall) -> None:
        """Accept the Phase 0 service contract without generating advice."""
        _first_store(hass)
        _LOGGER.debug(
            "Homekeep recommendation refresh requested before recommendation logic exists: force=%s area_id=%s entity_id=%s",
            call.data.get(ATTR_FORCE),
            call.data.get(ATTR_AREA_ID),
            call.data.get(ATTR_ENTITY_ID),
        )

    async def handle_dismiss_recommendation(call: ServiceCall) -> None:
        """Accept the Phase 0 dismissal contract without mutating recommendations."""
        _first_store(hass)
        _LOGGER.debug(
            "Homekeep recommendation dismissal requested before recommendation logic exists: recommendation_id=%s reason=%s",
            call.data[ATTR_RECOMMENDATION_ID],
            call.data.get(ATTR_REASON),
        )

    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH_RECOMMENDATIONS,
        handle_refresh_recommendations,
        schema=vol.Schema(
            {
                vol.Optional(ATTR_FORCE, default=False): cv.boolean,
                vol.Optional(ATTR_AREA_ID): cv.string,
                vol.Optional(ATTR_ENTITY_ID): cv.entity_id,
            }
        ),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_DISMISS_RECOMMENDATION,
        handle_dismiss_recommendation,
        schema=vol.Schema(
            {
                vol.Required(ATTR_RECOMMENDATION_ID): cv.string,
                vol.Optional(ATTR_REASON, default=""): cv.string,
            }
        ),
    )
    _LOGGER.debug("Registered Homekeep Phase 0 services")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Homekeep from a config entry."""
    store = HomekeepStorage(hass, entry)
    await store.async_load()

    _entry_stores(hass)[entry.entry_id] = store
    if PLATFORMS:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.info("Homekeep entry loaded")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Homekeep config entry."""
    unload_ok = True
    if PLATFORMS:
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        _entry_stores(hass).pop(entry.entry_id, None)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN, None)
    return unload_ok
