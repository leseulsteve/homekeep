"""Phase 0 scaffold checks for Homekeep."""

from __future__ import annotations

import json
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from custom_components.homekeep.const import (
    DATA_PRODUCING_SERVICES,
    OPTIONAL_RESPONSE_SERVICES,
    PLATFORMS,
    SERVICE_GENERATE_SMART_CHORE_LIST,
    SERVICE_CREATE_CHORE,
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
        self.assertNotIn("OPTION_DEV_MODE", source)
        self.assertNotIn("DEFAULT_DEV_MODE", source)
        self.assertNotIn("selector.BooleanSelector()", source)
        self.assertIn("OPTION_CALENDAR_ENTITY_IDS", source)
        self.assertIn('domain="calendar"', source)

    def test_services_are_registered_with_response_support(self) -> None:
        from custom_components.homekeep import _build_service_schemas

        source = (HOMEKEEP / "__init__.py").read_text()
        services = (HOMEKEEP / "services.yaml").read_text()
        schemas = self._build_service_schemas_without_home_assistant(
            _build_service_schemas
        )

        self.assertIn("supports_response", source)
        self.assertIn("SupportsResponse.ONLY", source)
        self.assertIn("SupportsResponse.OPTIONAL", source)
        self.assertIn(SERVICE_GENERATE_SMART_CHORE_LIST, DATA_PRODUCING_SERVICES)
        self.assertIn(SERVICE_START_RECOMMENDATION, DATA_PRODUCING_SERVICES)
        self.assertIn(SERVICE_CREATE_CHORE, OPTIONAL_RESPONSE_SERVICES)
        self.assertIn("complete_chore", OPTIONAL_RESPONSE_SERVICES)
        self.assertIn("generate_smart_chore_list:", services)
        self.assertIn("start_recommendation:", services)
        self.assertIn("create_chore:", services)
        self.assertIn(SERVICE_CREATE_CHORE, schemas)
        self.assertNotIn("load_sample_chores:", services)
        self.assertNotIn("answer_session_question:", services)
        self.assertIn("_service_handler(hass, service_name)", source)
        self.assertNotIn("implemented\": False", source)

    def _build_service_schemas_without_home_assistant(self, build_schemas):
        vol = types.ModuleType("voluptuous")
        vol.Schema = lambda schema: schema
        vol.Optional = lambda key, default=None: ("optional", key, default)
        vol.Required = lambda key: ("required", key)
        vol.In = lambda values: ("in", tuple(values))
        vol.Any = lambda *values: ("any", values)
        vol.Coerce = lambda value_type: ("coerce", value_type)
        vol.All = lambda *validators: ("all", validators)
        vol.Range = lambda **kwargs: ("range", tuple(sorted(kwargs.items())))

        cv = types.ModuleType("config_validation")
        cv.string = str
        cv.positive_int = int
        cv.boolean = bool

        homeassistant = types.ModuleType("homeassistant")
        helpers = types.ModuleType("homeassistant.helpers")
        helpers.config_validation = cv

        modules = {
            "voluptuous": vol,
            "homeassistant": homeassistant,
            "homeassistant.helpers": helpers,
            "homeassistant.helpers.config_validation": cv,
        }
        with patch.dict("sys.modules", modules):
            return build_schemas()

    def test_phase5_platforms_are_declared(self) -> None:
        self.assertEqual(PLATFORMS, ["sensor", "binary_sensor", "todo"])

    def test_home_assistant_storage_adapter_uses_versioned_store(self) -> None:
        source = (HOMEKEEP / "storage.py").read_text()

        self.assertIn("class HomekeepStorage", source)
        self.assertIn("Store(", source)
        self.assertIn("CURRENT_STORAGE_VERSION", source)
        self.assertIn("load_store_dict(raw)", source)
        self.assertIn("dump_store_dict(self.store)", source)


if __name__ == "__main__":
    unittest.main()
