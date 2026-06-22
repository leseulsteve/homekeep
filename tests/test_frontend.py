"""Tests for the Homekeep sidebar frontend registration."""

from __future__ import annotations

import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from custom_components.homekeep import frontend as homekeep_frontend


class FakeHttp:
    def __init__(self) -> None:
        self.static_paths: list[object] = []

    async def async_register_static_paths(self, configs: list[object]) -> None:
        self.static_paths.extend(configs)


class FrontendRegistrationTest(unittest.IsolatedAsyncioTestCase):
    async def test_register_frontend_uses_non_iframe_custom_panel(self) -> None:
        calls: dict[str, object] = {}

        class StaticPathConfig:
            def __init__(
                self, url_path: str, path: str, cache_headers: bool = True
            ) -> None:
                self.url_path = url_path
                self.path = path
                self.cache_headers = cache_headers

        fake_frontend = types.ModuleType("homeassistant.components.frontend")
        fake_frontend.async_register_built_in_panel = (
            lambda hass, **kwargs: calls.setdefault("panel", kwargs)
        )

        fake_http = types.ModuleType("homeassistant.components.http")
        fake_http.StaticPathConfig = StaticPathConfig

        modules = self._home_assistant_modules(fake_frontend, fake_http)
        hass = SimpleNamespace(http=FakeHttp())

        with patch.dict(sys.modules, modules):
            await homekeep_frontend.async_register_frontend(hass)

        self.assertEqual(len(hass.http.static_paths), 1)
        static_path = hass.http.static_paths[0]
        self.assertEqual(static_path.url_path, "/homekeep_static/homekeep-panel.js")
        self.assertEqual(Path(static_path.path).name, "homekeep-panel.js")
        self.assertFalse(static_path.cache_headers)

        panel = calls["panel"]
        self.assertEqual(panel["component_name"], "custom")
        self.assertEqual(panel["frontend_url_path"], "homekeep")
        self.assertTrue(panel["update"])
        custom_config = panel["config"]["_panel_custom"]
        self.assertEqual(custom_config["name"], "homekeep-panel")
        self.assertEqual(custom_config["module_url"], "/homekeep_static/homekeep-panel.js")
        self.assertFalse(custom_config["embed_iframe"])
        self.assertFalse(custom_config["trust_external"])
        self.assertTrue(panel["config"]["mock_ready_now"])

    def test_unregister_frontend_removes_panel(self) -> None:
        removed: dict[str, object] = {}
        fake_frontend = types.ModuleType("homeassistant.components.frontend")
        fake_frontend.async_remove_panel = (
            lambda hass, path, **kwargs: removed.update({"path": path, **kwargs})
        )
        modules = self._home_assistant_modules(fake_frontend, None)

        with patch.dict(sys.modules, modules):
            homekeep_frontend.async_unregister_frontend(SimpleNamespace())

        self.assertEqual(removed["path"], "homekeep")
        self.assertFalse(removed["warn_if_unknown"])

    def _home_assistant_modules(
        self, fake_frontend: types.ModuleType, fake_http: types.ModuleType | None
    ) -> dict[str, types.ModuleType]:
        homeassistant = types.ModuleType("homeassistant")
        components = types.ModuleType("homeassistant.components")
        components.frontend = fake_frontend
        modules = {
            "homeassistant": homeassistant,
            "homeassistant.components": components,
            "homeassistant.components.frontend": fake_frontend,
        }
        if fake_http is not None:
            components.http = fake_http
            modules["homeassistant.components.http"] = fake_http
        return modules


if __name__ == "__main__":
    unittest.main()
