"""Small bilingual text-signal helpers for local keyword inference."""

from __future__ import annotations

import unicodedata


CALENDAR_GUEST_KEYWORDS = (
    "guest",
    "visitor",
    "visit",
    "dinner",
    "party",
    "invite",
    "invité",
    "invites",
    "invités",
    "visite",
    "souper",
    "dîner",
    "diner",
    "recevoir",
)
CALENDAR_TRAVEL_KEYWORDS = (
    "travel",
    "airport",
    "leave home",
    "drive",
    "voyage",
    "aéroport",
    "aeroport",
    "partir",
    "départ",
    "depart",
    "conduire",
)
TRASH_KEYWORDS = (
    "trash",
    "garbage",
    "recycling",
    "compost",
    "poubelle",
    "poubelles",
    "vidange",
    "vidanges",
    "déchet",
    "déchets",
    "dechet",
    "dechets",
    "recyclage",
    "compostage",
)
GUEST_PREP_CHORE_KEYWORDS = (
    "bathroom",
    "guest",
    "entry",
    "surface",
    "kitchen",
    "salle de bain",
    "toilette",
    "toilettes",
    "invité",
    "invites",
    "invités",
    "visiteur",
    "visiteurs",
    "entrée",
    "entree",
    "surface",
    "comptoir",
    "comptoirs",
    "cuisine",
)


def normalize_guess_text(value: str) -> str:
    """Normalize user-facing text before conservative keyword matching."""

    normalized = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def has_any_keyword(text: str, keywords: tuple[str, ...]) -> bool:
    """Return true when normalized text includes one normalized keyword."""

    normalized = normalize_guess_text(text)
    return any(normalize_guess_text(keyword) in normalized for keyword in keywords)
