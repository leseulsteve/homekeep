"""Phase 0 scaffold checks for Homekeep."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from custom_components.homekeep.const import (
    DATA_PRODUCING_SERVICES,
    OPTIONAL_RESPONSE_SERVICES,
    SERVICE_GENERATE_SMART_CHORE_LIST,
    SERVICE_START_RECOMMENDATION,
)


ROOT = Path(__file__).parents[1]
HOMEKEEP = ROOT / "custom_components" / "homekeep"


class HomekeepScaffoldTest(unittest.TestCase):
    """Keep the scaffold importable, versioned, and service-wired."""

    def test_manifest_declares_custom_integration_shape(self) -> None:
        manifest = json.loads((HOMEKEEP / "manifest.json").read_text())

        self.assertEqual(manifest["domain"], "homekeep")
        self.assertEqual(manifest["name"], "Homekeep")
        self.assertTrue(manifest["config_flow"])
        self.assertTrue(manifest["single_config_entry"])
        self.assertIn("python-dateutil", manifest["requirements"][0])

    def test_config_flow_is_single_instance_and_versioned(self) -> None:
        source = (HOMEKEEP / "config_flow.py").read_text()

        self.assertIn("class HomekeepConfigFlow", source)
        self.assertIn("VERSION = 1", source)
        self.assertIn("single_instance_allowed", source)
        self.assertIn("async_create_entry(title=NAME, data={})", source)

    def test_services_are_registered_with_response_support(self) -> None:
        source = (HOMEKEEP / "__init__.py").read_text()
        services = (HOMEKEEP / "services.yaml").read_text()

        self.assertIn("supports_response", source)
        self.assertIn("SupportsResponse.ONLY", source)
        self.assertIn("SupportsResponse.OPTIONAL", source)
        self.assertIn(SERVICE_GENERATE_SMART_CHORE_LIST, DATA_PRODUCING_SERVICES)
        self.assertIn(SERVICE_START_RECOMMENDATION, DATA_PRODUCING_SERVICES)
        self.assertIn("complete_chore", OPTIONAL_RESPONSE_SERVICES)
        self.assertIn("generate_smart_chore_list:", services)
        self.assertIn("start_recommendation:", services)
        self.assertNotIn("answer_session_question:", services)

    def test_home_assistant_storage_adapter_uses_versioned_store(self) -> None:
        source = (HOMEKEEP / "storage.py").read_text()

        self.assertIn("class HomekeepStorage", source)
        self.assertIn("Store(", source)
        self.assertIn("CURRENT_STORAGE_VERSION", source)
        self.assertIn("load_store_dict(raw)", source)
        self.assertIn("dump_store_dict(self.store)", source)


if __name__ == "__main__":
    unittest.main()
