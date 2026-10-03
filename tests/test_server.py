from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from ai_workbench_mcp import __version__
from ai_workbench_mcp import server


def req(method: str, params=None, rpc_id=1):
    return {"jsonrpc": "2.0", "id": rpc_id, "method": method, "params": params or {}}


class ServerTests(unittest.TestCase):
    def initialized_server(self):
        instance = server.CatalogServer(server.load_catalog())
        instance.handle(req("initialize", {"protocolVersion": "2025-06-18"}))
        instance.handle({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return instance

    def test_every_public_tool_has_complete_read_only_hints(self):
        required = {"readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint"}
        self.assertEqual(3, len(server.TOOLS))
        for tool in server.TOOLS:
            annotations = tool["annotations"]
            self.assertTrue(required <= set(annotations), tool["name"])
            self.assertTrue(annotations["readOnlyHint"])
            self.assertFalse(annotations["destructiveHint"])
            self.assertTrue(annotations["idempotentHint"])
            self.assertFalse(annotations["openWorldHint"])

    def test_list_prompts_by_public_name(self):
        result = self.initialized_server().handle(
            req("tools/call", {"name": "list_prompts", "arguments": {}})
        )["result"]
        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertTrue(payload["prompts"])
        self.assertTrue(payload["assistants"])

    def test_render_prompt_by_public_name(self):
        catalog = server.load_catalog()
        entry = catalog["prompts"][0]
        result = self.initialized_server().handle(
            req(
                "tools/call",
                {
                    "name": "render_prompt",
                    "arguments": {"id": entry["id"], "variables": entry["example"]},
                },
            )
        )["result"]
        self.assertFalse(result["isError"])
        self.assertTrue(result["content"][0]["text"].strip())

    def test_get_assistant_by_public_name(self):
        assistant_id = server.load_catalog()["assistants"][0]["id"]
        result = self.initialized_server().handle(
            req(
                "tools/call",
                {
                    "name": "get_assistant",
                    "arguments": {"id": assistant_id, "target": "chatgpt"},
                },
            )
        )["result"]
        self.assertFalse(result["isError"])
        self.assertIn("## Instructions", result["content"][0]["text"])

    def test_unknown_tool_is_bounded_error(self):
        result = self.initialized_server().handle(
            req("tools/call", {"name": "run_shell", "arguments": {"command": "whoami"}})
        )["result"]
        self.assertTrue(result["isError"])

    def test_server_imports_no_network_or_process_modules(self):
        path = SRC / "ai_workbench_mcp" / "server.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        allowed = {"json", "re", "sys", "importlib", "typing", "__future__"}
        self.assertTrue(imported <= allowed, imported)

    def test_real_stdio_handshake(self):
        messages = [
            req("initialize", {"protocolVersion": "2025-06-18"}),
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            req("tools/list", rpc_id=2),
        ]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC) + os.pathsep + env.get("PYTHONPATH", "")
        result = subprocess.run(
            [sys.executable, "-m", "ai_workbench_mcp.server"],
            input="\n".join(json.dumps(message) for message in messages) + "\n",
            text=True,
            capture_output=True,
            timeout=10,
            env=env,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        lines = result.stdout.splitlines()
        self.assertEqual(2, len(lines))
        self.assertEqual(__version__, json.loads(lines[0])["result"]["serverInfo"]["version"])
        self.assertEqual(3, len(json.loads(lines[1])["result"]["tools"]))


if __name__ == "__main__":
    unittest.main()
