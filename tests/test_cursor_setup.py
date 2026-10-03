from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "examples" / "cursor-mcp.json"
GUIDE = ROOT / "CURSOR-SETUP.md"
GUIDE_TR = ROOT / "CURSOR-SETUP_TR.md"


class CursorSetupTests(unittest.TestCase):
    def test_checked_in_cursor_config_is_minimal_stdio(self):
        payload = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.assertEqual({"mcpServers"}, set(payload))
        server = payload["mcpServers"]["ai-workbench-mcp"]
        self.assertEqual("stdio", server["type"])
        self.assertEqual("python", server["command"])
        self.assertEqual(["-m", "ai_workbench_mcp.server"], server["args"])
        self.assertNotIn("env", server)
        self.assertNotIn("url", server)
        self.assertNotIn("headers", server)

    def test_cursor_guides_pin_release_and_cover_all_public_tools(self):
        for path in (GUIDE, GUIDE_TR):
            text = path.read_text(encoding="utf-8")
            self.assertIn("alptugharun-ai-workbench-mcp==0.1.0a1", text)
            self.assertIn("list_prompts", text)
            self.assertIn("render_prompt", text)
            self.assertIn("get_assistant", text)
            self.assertIn("python -m ai_workbench_mcp.server", text)

    def test_cursor_guide_keeps_host_evidence_bounded(self):
        text = GUIDE.read_text(encoding="utf-8")
        self.assertIn("does not prove compatibility with every MCP client", text)
        self.assertIn("Do not accept a green connection badge as the final proof", text)


if __name__ == "__main__":
    unittest.main()
