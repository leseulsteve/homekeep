"""Phase 0 scaffold checks for Homekeep."""

from pathlib import Path
import json
import unittest


ROOT = Path(__file__).parents[1]
HOMEKEEP = ROOT / "custom_components/homekeep"


class TestHomekeepScaffold(unittest.TestCase):
    """Keep the Homekeep scaffold empty, versioned, and service-wired."""

    def test_manifest_declares_config_flow_without_runtime_requirements(self) -> None:
        manifest = json.loads((HOMEKEEP / "manifest.json").read_text())
        self.assertEqual("homekeep", manifest["domain"])
        self.assertEqual("Homekeep", manifest["name"])
        self.assertTrue(manifest["config_flow"])
        self.assertEqual([], manifest["requirements"])

    def test_config_flow_is_single_instance_and_versioned(self) -> None:
        source = (HOMEKEEP / "config_flow.py").read_text()
        self.assertIn("class HomekeepConfigFlow", source)
        self.assertIn("VERSION = 1", source)
        self.assertIn("single_instance_allowed", source)
        self.assertIn("async_create_entry(title=NAME, data={})", source)

    def test_storage_helper_has_empty_versioned_shape(self) -> None:
        source = (HOMEKEEP / "store.py").read_text()
        const_source = (HOMEKEEP / "const.py").read_text()
        self.assertIn("STORAGE_VERSION = 1", const_source)
        self.assertIn("Store(", source)
        self.assertIn("f\"{DOMAIN}.{entry.entry_id}\"", source)
        self.assertIn("def empty_store()", source)
        self.assertIn('"recommendations": {}', source)
        self.assertIn('"dismissed_recommendations": {}', source)
        self.assertIn('"last_refresh": None', source)

    def test_services_are_registered_with_schemas_but_no_recommendation_logic(self) -> None:
        source = (HOMEKEEP / "__init__.py").read_text()
        services = (HOMEKEEP / "services.yaml").read_text()
        self.assertIn("SERVICE_REFRESH_RECOMMENDATIONS", source)
        self.assertIn("SERVICE_DISMISS_RECOMMENDATION", source)
        self.assertIn("schema=vol.Schema", source)
        self.assertIn("vol.Optional(ATTR_FORCE, default=False): cv.boolean", source)
        self.assertIn("vol.Required(ATTR_RECOMMENDATION_ID): cv.string", source)
        self.assertIn("HomekeepStorage(hass, entry)", source)
        self.assertNotIn("async_generate", source)
        self.assertIn("refresh_recommendations:", services)
        self.assertIn("dismiss_recommendation:", services)


if __name__ == "__main__":
    unittest.main()
