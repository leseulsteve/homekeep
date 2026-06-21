"""Tests for Homekeep models and validation helpers."""

from __future__ import annotations

import math
import unittest

from custom_components.homekeep.models import (
    ChoreDefinition,
    HomekeepValidationError,
    resolve_completed_by,
)


def valid_chore_data() -> dict:
    return {
        "name": "Wipe counters",
        "area_id": "kitchen",
        "group_id": "surfaces",
        "base_interval_days": 2,
        "min_interval_days": 1,
        "max_interval_days": 5,
        "estimated_minutes": 5,
        "energy": "normal",
        "visibility": "high",
        "health_weight": 1.2,
        "variants": {"normal": {"label": "Wipe counters", "credit": 1.0}},
        "pairs_with": [],
        "enabled": True,
    }


class ChoreDefinitionValidationTest(unittest.TestCase):
    def test_invalid_non_finite_interval_is_rejected(self) -> None:
        data = valid_chore_data()
        data["base_interval_days"] = math.inf

        with self.assertRaisesRegex(HomekeepValidationError, "base_interval_days"):
            ChoreDefinition.from_dict("wipe_counters", data)

    def test_invalid_interval_order_is_rejected(self) -> None:
        data = valid_chore_data()
        data["min_interval_days"] = 3

        with self.assertRaisesRegex(
            HomekeepValidationError, "min_interval_days must be <= base_interval_days"
        ):
            ChoreDefinition.from_dict("wipe_counters", data)

    def test_variant_key_must_be_known(self) -> None:
        data = valid_chore_data()
        data["variants"]["medium"] = {"label": "Medium clean", "credit": 1.0}

        with self.assertRaisesRegex(HomekeepValidationError, "variant keys"):
            ChoreDefinition.from_dict("wipe_counters", data)

    def test_enabled_chore_requires_normal_variant(self) -> None:
        data = valid_chore_data()
        data["variants"] = {"tiny": {"label": "Tiny", "credit": 0.5}}

        with self.assertRaisesRegex(HomekeepValidationError, "normal variant"):
            ChoreDefinition.from_dict("wipe_counters", data)

    def test_variant_credit_must_be_within_bounds(self) -> None:
        data = valid_chore_data()
        data["variants"]["normal"]["credit"] = 2.5

        with self.assertRaisesRegex(HomekeepValidationError, "0.1 and 2.0"):
            ChoreDefinition.from_dict("wipe_counters", data)

    def test_completed_by_must_match_participants_when_present(self) -> None:
        with self.assertRaisesRegex(HomekeepValidationError, "participant"):
            resolve_completed_by(["person.alex"], "person.alex", "person.steve")

    def test_completed_by_defaults_to_started_by(self) -> None:
        self.assertEqual(
            resolve_completed_by(["person.steve"], "person.steve", None),
            "person.steve",
        )


if __name__ == "__main__":
    unittest.main()
