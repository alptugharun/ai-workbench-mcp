from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RegistryMetadataTests(unittest.TestCase):
    def test_server_json_matches_python_package(self):
        server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        project_name = re.search(r'^name\s*=\s*"([^"]+)"', pyproject, re.M).group(1)
        project_version = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M).group(1)

        self.assertEqual("io.github.alptugharun/ai-workbench-mcp", server["name"])
        self.assertEqual(project_version, server["version"])
        self.assertEqual(1, len(server["packages"]))

        package = server["packages"][0]
        self.assertEqual("pypi", package["registryType"])
        self.assertEqual("https://pypi.org", package["registryBaseUrl"])
        self.assertEqual(project_name, package["identifier"])
        self.assertEqual(project_version, package["version"])
        self.assertEqual("uvx", package["runtimeHint"])
        self.assertEqual({"type": "stdio"}, package["transport"])

    def test_pypi_readme_contains_registry_ownership_marker(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "mcp-name: io.github.alptugharun/ai-workbench-mcp",
            readme,
        )


if __name__ == "__main__":
    unittest.main()
