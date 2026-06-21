"""Constants for the Homekeep integration."""

from __future__ import annotations

DOMAIN = "homekeep"
NAME = "Homekeep"

PLATFORMS: list[str] = []

SERVICE_REFRESH_RECOMMENDATIONS = "refresh_recommendations"
SERVICE_DISMISS_RECOMMENDATION = "dismiss_recommendation"

ATTR_RECOMMENDATION_ID = "recommendation_id"
ATTR_AREA_ID = "area_id"
ATTR_ENTITY_ID = "entity_id"
ATTR_FORCE = "force"
ATTR_REASON = "reason"

STORAGE_KEY = DOMAIN
STORAGE_VERSION = 1
