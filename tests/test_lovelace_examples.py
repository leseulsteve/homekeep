"""Tests for Homekeep Lovelace example artifacts."""

from __future__ import annotations

import unittest
from pathlib import Path

from custom_components.homekeep.const import SOURCES


ROOT = Path(__file__).resolve().parents[1]


class LovelaceExamplesTest(unittest.TestCase):
    def test_lovelace_source_is_supported(self) -> None:
        self.assertIn("lovelace", SOURCES)
        self.assertNotIn("bubble_card", SOURCES)

    def test_dashboard_uses_stock_lovelace_cards(self) -> None:
        dashboard = (ROOT / "examples" / "lovelace_dashboard.yaml").read_text(
            encoding="utf-8"
        )

        self.assertIn("lovelace_dashboard:", dashboard)
        self.assertIn("type: sections", dashboard)
        self.assertIn("type: tile", dashboard)
        self.assertIn("type: todo-list", dashboard)
        self.assertIn("color: teal", dashboard)
        self.assertIn("state_not: \"\"", dashboard)
        self.assertIn("script.homekeep_create_chore_from_view", dashboard)
        self.assertIn("homekeep.create_chore", dashboard)
        self.assertNotIn("custom:bubble-card", dashboard)
        self.assertNotIn("bubble_card", dashboard)

    def test_single_recipe_uses_lovelace_completion_source(self) -> None:
        recipe = (ROOT / "examples" / "lovelace_dashboard.yaml").read_text(
            encoding="utf-8"
        )

        self.assertIn("source: lovelace", recipe)
        self.assertNotIn("source: bubble_card", recipe)


if __name__ == "__main__":
    unittest.main()
