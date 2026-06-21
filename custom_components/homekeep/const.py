"""Constants for Homekeep."""

DOMAIN = "homekeep"
NAME = "Homekeep"
PLATFORMS: list[str] = ["sensor", "binary_sensor", "todo"]

CURRENT_STORAGE_VERSION = 2
STORAGE_KEY = f"{DOMAIN}.store"

OPTION_DEV_MODE = "dev_mode"

SERVICE_GENERATE_SMART_CHORE_LIST = "generate_smart_chore_list"
SERVICE_START_RECOMMENDATION = "start_recommendation"
SERVICE_START_CHORE_BUNDLE = "start_chore_bundle"
SERVICE_COMPLETE_CHORE = "complete_chore"
SERVICE_SKIP_CHORE = "skip_chore"
SERVICE_SNOOZE_CHORE = "snooze_chore"
SERVICE_DISMISS_CHORE = "dismiss_chore"
SERVICE_REFRESH_CALENDAR_CONTEXT = "refresh_calendar_context"
SERVICE_LOAD_SAMPLE_CHORES = "load_sample_chores"
SERVICE_PAUSE_SESSION = "pause_session"
SERVICE_ACCEPT_BONUS_CHORE = "accept_bonus_chore"
SERVICE_END_SESSION = "end_session"

DATA_PRODUCING_SERVICES = {
    SERVICE_GENERATE_SMART_CHORE_LIST,
    SERVICE_START_RECOMMENDATION,
    SERVICE_START_CHORE_BUNDLE,
    SERVICE_ACCEPT_BONUS_CHORE,
    SERVICE_END_SESSION,
}

OPTIONAL_RESPONSE_SERVICES = {
    SERVICE_COMPLETE_CHORE,
    SERVICE_SKIP_CHORE,
    SERVICE_SNOOZE_CHORE,
    SERVICE_DISMISS_CHORE,
    SERVICE_REFRESH_CALENDAR_CONTEXT,
    SERVICE_LOAD_SAMPLE_CHORES,
    SERVICE_PAUSE_SESSION,
}

ATTR_AREA_ID = "area_id"
ATTR_BUNDLE_ID = "bundle_id"
ATTR_CALENDAR_ENTITY_IDS = "calendar_entity_ids"
ATTR_CHORE_ID = "chore_id"
ATTR_COMPLETED_BY = "completed_by"
ATTR_ENERGY_LEVEL = "energy_level"
ATTR_GOAL = "goal"
ATTR_INCLUDE_ALTERNATES = "include_alternates"
ATTR_INFER_MOOD = "infer_mood"
ATTR_MOOD = "mood"
ATTR_OFFER_BONUS_CHORE = "offer_bonus_chore"
ATTR_REASON = "reason"
ATTR_RECOMMENDATION_ID = "recommendation_id"
ATTR_RECOMMENDATION_MODE = "recommendation_mode"
ATTR_RECOMMENDATION_SNAPSHOT_ID = "recommendation_snapshot_id"
ATTR_REPLACE_EXISTING = "replace_existing"
ATTR_REQUEST_ID = "request_id"
ATTR_SESSION_ID = "session_id"
ATTR_SESSION_ITEM_ID = "session_item_id"
ATTR_SNOOZE_MINUTES = "snooze_minutes"
ATTR_SOURCE = "source"
ATTR_STATUS = "status"
ATTR_TARGET_TIME_WINDOW = "target_time_window"
ATTR_TIME_BUDGET_MINUTES = "time_budget_minutes"
ATTR_USER_ID = "user_id"
ATTR_VARIANT = "variant"

ENERGY_LEVELS = ["low", "normal", "high", "quiet"]
GOALS = ["quick_wins", "overdue", "visible_impact", "prevent_future_mess", "full_reset"]
MOODS = ["unknown", "calm", "focused", "tired", "overwhelmed", "energized", "auto"]
RECOMMENDATION_MODES = ["ready_now", "scheduled_suggestion"]
SESSION_END_STATUSES = ["completed", "cancelled"]
SOURCES = ["service", "todo", "bubble_card", "voice", "automation"]
VARIANTS = ["tiny", "normal", "deep"]
