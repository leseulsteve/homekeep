"""The Homekeep integration."""

from __future__ import annotations

from typing import Any, Callable

from .const import (
    ATTR_AREA_ID,
    ATTR_BASE_INTERVAL_DAYS,
    ATTR_BUNDLE_ID,
    ATTR_CALENDAR_ENTITY_IDS,
    ATTR_CHORE_ID,
    ATTR_COMPLETED_BY,
    ATTR_ENERGY_LEVEL,
    ATTR_ESTIMATED_MINUTES,
    ATTR_GOAL,
    ATTR_GROUP_ID,
    ATTR_HEALTH_WEIGHT,
    ATTR_INCLUDE_ALTERNATES,
    ATTR_INFER_MOOD,
    ATTR_MAX_INTERVAL_DAYS,
    ATTR_MIN_INTERVAL_DAYS,
    ATTR_MOOD,
    ATTR_NAME,
    ATTR_OFFER_BONUS_CHORE,
    ATTR_REASON,
    ATTR_RECOMMENDATION_ID,
    ATTR_RECOMMENDATION_MODE,
    ATTR_RECOMMENDATION_SNAPSHOT_ID,
    ATTR_REQUEST_ID,
    ATTR_SESSION_ID,
    ATTR_SESSION_ITEM_ID,
    ATTR_SNOOZE_MINUTES,
    ATTR_SOURCE,
    ATTR_STATUS,
    ATTR_TARGET_TIME_WINDOW,
    ATTR_TIME_BUDGET_MINUTES,
    ATTR_USER_ID,
    ATTR_VARIANT,
    ATTR_VISIBILITY,
    DATA_PRODUCING_SERVICES,
    DOMAIN,
    ENERGY_LEVELS,
    GOALS,
    MOODS,
    OPTIONAL_RESPONSE_SERVICES,
    PLATFORMS,
    RECOMMENDATION_MODES,
    SERVICE_ACCEPT_BONUS_CHORE,
    SERVICE_COMPLETE_CHORE,
    SERVICE_CREATE_CHORE,
    SERVICE_DISMISS_CHORE,
    SERVICE_END_SESSION,
    SERVICE_GENERATE_SMART_CHORE_LIST,
    SERVICE_PAUSE_SESSION,
    SERVICE_REFRESH_CALENDAR_CONTEXT,
    SERVICE_SKIP_CHORE,
    SERVICE_SNOOZE_CHORE,
    SERVICE_START_CHORE_BUNDLE,
    SERVICE_START_RECOMMENDATION,
    SESSION_END_STATUSES,
    SOURCES,
    VARIANTS,
    VISIBILITIES,
)
from .models import HomekeepValidationError
from .storage import HomekeepStorage


def _entry_stores(hass: Any) -> dict[str, HomekeepStorage]:
    """Return Homekeep entry storage instances."""

    return hass.data.setdefault(DOMAIN, {})


async def async_setup(hass: Any, config: dict[str, Any]) -> bool:
    """Set up Homekeep services."""

    from homeassistant.core import SupportsResponse

    schemas = _build_service_schemas()
    for service_name, schema in schemas.items():
        response_support = None
        if service_name in DATA_PRODUCING_SERVICES:
            response_support = SupportsResponse.ONLY
        elif service_name in OPTIONAL_RESPONSE_SERVICES:
            response_support = SupportsResponse.OPTIONAL

        register_kwargs: dict[str, Any] = {"schema": schema}
        if response_support is not None:
            register_kwargs["supports_response"] = response_support

        hass.services.async_register(
            DOMAIN,
            service_name,
            _service_handler(hass, service_name),
            **register_kwargs,
        )

    return True


async def async_setup_entry(hass: Any, entry: Any) -> bool:
    """Set up Homekeep from a config entry."""

    storage = HomekeepStorage(hass, entry)
    await storage.async_load()
    _entry_stores(hass)[entry.entry_id] = storage
    storage.calendar_unsub = _async_setup_calendar_listeners(hass, storage, entry)

    if PLATFORMS:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: Any, entry: Any) -> bool:
    """Unload a Homekeep config entry."""

    unload_ok = True
    if PLATFORMS:
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        stores = hass.data.get(DOMAIN, {})
        storage = stores.get(entry.entry_id)
        if storage is not None:
            unsub = getattr(storage, "calendar_unsub", None)
            if unsub:
                unsub()
        stores.pop(entry.entry_id, None)
        if not stores:
            hass.data.pop(DOMAIN, None)

    return unload_ok


def _service_handler(hass: Any, service_name: str) -> Callable[[Any], Any]:
    """Return a Home Assistant service handler."""

    async def handle_service(call: Any) -> dict[str, Any] | None:
        from .runtime import HomekeepServiceRuntime

        try:
            runtime = HomekeepServiceRuntime(_first_storage(hass), hass)
            response = await runtime.async_handle(service_name, dict(call.data))
        except HomekeepValidationError as err:
            raise _service_validation_error(str(err)) from err

        if service_name in DATA_PRODUCING_SERVICES:
            return response or {}
        if getattr(call, "return_response", False):
            return response or {"status": "ok"}
        return None

    return handle_service


def _first_storage(hass: Any) -> HomekeepStorage:
    stores = hass.data.get(DOMAIN, {})
    if not stores:
        raise HomekeepValidationError("Homekeep is not loaded")
    return next(iter(stores.values()))


def _service_validation_error(message: str) -> Exception:
    try:
        from homeassistant.exceptions import ServiceValidationError
    except ModuleNotFoundError:
        return HomekeepValidationError(message)
    return ServiceValidationError(message)


def _async_setup_calendar_listeners(hass: Any, storage: HomekeepStorage, entry: Any) -> Any:
    """Listen for selected calendar entity state changes."""

    from homeassistant.helpers.event import async_track_state_change_event

    from .calendar_context import (
        invalidate_calendar_context_for_entity,
        selected_calendar_entity_ids,
    )

    entity_ids = selected_calendar_entity_ids(entry)
    if not entity_ids:
        return None

    async def calendar_changed(event: Any) -> None:
        entity_id = event.data.get("entity_id")
        if not entity_id:
            return
        if invalidate_calendar_context_for_entity(storage.store, entity_id):
            await storage.async_save()

    return async_track_state_change_event(hass, entity_ids, calendar_changed)


def _build_service_schemas() -> dict[str, Any]:
    """Build Home Assistant service schemas lazily so tests can run without HA."""

    import voluptuous as vol
    from homeassistant.helpers import config_validation as cv

    optional_string = cv.string
    nullable_string = vol.Any(None, cv.string)

    return {
        SERVICE_GENERATE_SMART_CHORE_LIST: vol.Schema(
            {
                vol.Optional(ATTR_USER_ID): nullable_string,
                vol.Optional(
                    ATTR_RECOMMENDATION_MODE, default="ready_now"
                ): vol.In(RECOMMENDATION_MODES),
                vol.Optional(ATTR_TARGET_TIME_WINDOW): nullable_string,
                vol.Optional(ATTR_TIME_BUDGET_MINUTES): vol.Any(None, cv.positive_int),
                vol.Optional(ATTR_ENERGY_LEVEL): vol.Any(None, vol.In(ENERGY_LEVELS)),
                vol.Optional(ATTR_GOAL): vol.Any(None, vol.In(GOALS)),
                vol.Optional(ATTR_AREA_ID): nullable_string,
                vol.Optional(ATTR_MOOD): vol.Any(None, vol.In(MOODS)),
                vol.Optional(ATTR_INFER_MOOD, default=True): cv.boolean,
                vol.Optional(ATTR_INCLUDE_ALTERNATES, default=True): cv.boolean,
                vol.Optional(ATTR_REQUEST_ID): nullable_string,
            }
        ),
        SERVICE_START_RECOMMENDATION: vol.Schema(
            {
                vol.Required(ATTR_RECOMMENDATION_SNAPSHOT_ID): cv.string,
                vol.Required(ATTR_RECOMMENDATION_ID): cv.string,
                vol.Optional(ATTR_USER_ID): nullable_string,
                vol.Optional(ATTR_REQUEST_ID): nullable_string,
            }
        ),
        SERVICE_START_CHORE_BUNDLE: vol.Schema(
            {
                vol.Required(ATTR_RECOMMENDATION_SNAPSHOT_ID): cv.string,
                vol.Required(ATTR_BUNDLE_ID): cv.string,
                vol.Optional(ATTR_USER_ID): nullable_string,
                vol.Optional(ATTR_REQUEST_ID): nullable_string,
            }
        ),
        SERVICE_CREATE_CHORE: vol.Schema(
            {
                vol.Optional(ATTR_CHORE_ID): cv.string,
                vol.Required(ATTR_NAME): cv.string,
                vol.Optional(ATTR_AREA_ID): nullable_string,
                vol.Optional(ATTR_GROUP_ID): nullable_string,
                vol.Optional(ATTR_BASE_INTERVAL_DAYS, default=7): vol.Coerce(float),
                vol.Optional(ATTR_MIN_INTERVAL_DAYS): vol.Coerce(float),
                vol.Optional(ATTR_MAX_INTERVAL_DAYS): vol.Coerce(float),
                vol.Optional(ATTR_ESTIMATED_MINUTES, default=10): cv.positive_int,
                vol.Optional(ATTR_ENERGY_LEVEL, default="normal"): vol.In(
                    ENERGY_LEVELS
                ),
                vol.Optional(ATTR_VISIBILITY, default="medium"): vol.In(VISIBILITIES),
                vol.Optional(ATTR_HEALTH_WEIGHT, default=1.0): vol.Coerce(float),
                vol.Optional(ATTR_REQUEST_ID): nullable_string,
            }
        ),
        SERVICE_COMPLETE_CHORE: vol.Schema(
            {
                vol.Required(ATTR_CHORE_ID): cv.string,
                vol.Optional(ATTR_SESSION_ID): nullable_string,
                vol.Optional(ATTR_SESSION_ITEM_ID): nullable_string,
                vol.Optional(ATTR_VARIANT, default="normal"): vol.In(VARIANTS),
                vol.Optional(ATTR_COMPLETED_BY): nullable_string,
                vol.Optional(ATTR_SOURCE, default="service"): vol.In(SOURCES),
                vol.Optional(ATTR_REQUEST_ID): nullable_string,
            }
        ),
        SERVICE_SKIP_CHORE: vol.Schema(_session_item_schema(cv, vol, nullable_string)),
        SERVICE_SNOOZE_CHORE: vol.Schema(
            {
                **_session_item_schema(cv, vol, nullable_string),
                vol.Required(ATTR_SNOOZE_MINUTES): vol.All(
                    cv.positive_int, vol.Range(min=5, max=1440)
                ),
            }
        ),
        SERVICE_DISMISS_CHORE: vol.Schema(
            {
                **_session_item_schema(cv, vol, nullable_string),
                vol.Optional(ATTR_RECOMMENDATION_SNAPSHOT_ID): nullable_string,
            }
        ),
        SERVICE_REFRESH_CALENDAR_CONTEXT: vol.Schema(
            {
                vol.Optional(ATTR_TARGET_TIME_WINDOW): nullable_string,
                vol.Optional(ATTR_CALENDAR_ENTITY_IDS): vol.Any(
                    None, [optional_string]
                ),
            }
        ),
        SERVICE_PAUSE_SESSION: vol.Schema(
            {
                vol.Required(ATTR_SESSION_ID): cv.string,
                vol.Optional(ATTR_REQUEST_ID): nullable_string,
            }
        ),
        SERVICE_ACCEPT_BONUS_CHORE: vol.Schema(
            {
                vol.Required(ATTR_SESSION_ID): cv.string,
                vol.Required(ATTR_CHORE_ID): cv.string,
                vol.Optional(ATTR_REQUEST_ID): nullable_string,
            }
        ),
        SERVICE_END_SESSION: vol.Schema(
            {
                vol.Required(ATTR_SESSION_ID): cv.string,
                vol.Required(ATTR_STATUS): vol.In(SESSION_END_STATUSES),
                vol.Optional(ATTR_OFFER_BONUS_CHORE, default=False): cv.boolean,
                vol.Optional(ATTR_REQUEST_ID): nullable_string,
            }
        ),
    }


def _session_item_schema(cv: Any, vol: Any, nullable_string: Any) -> dict[Any, Any]:
    return {
        vol.Required(ATTR_CHORE_ID): cv.string,
        vol.Optional(ATTR_SESSION_ID): nullable_string,
        vol.Optional(ATTR_SESSION_ITEM_ID): nullable_string,
        vol.Optional(ATTR_REASON): nullable_string,
        vol.Optional(ATTR_REQUEST_ID): nullable_string,
    }
