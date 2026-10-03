from __future__ import annotations

import json
import subprocess
import sys


def request(method: str, params: dict | None = None, rpc_id: int = 1) -> dict:
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "method": method,
        "params": params or {},
    }


def main() -> int:
    messages = [
        request("initialize", {"protocolVersion": "2025-06-18"}),
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        request("tools/list", rpc_id=2),
    ]
    result = subprocess.run(
        [sys.executable, "-m", "ai_workbench_mcp.server"],
        input="\n".join(json.dumps(message) for message in messages) + "\n",
        text=True,
        capture_output=True,
        timeout=10,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode

    lines = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    if len(lines) != 2:
        print("Unexpected MCP response count.", file=sys.stderr)
        return 2

    init, tools = lines
    names = [tool["name"] for tool in tools["result"]["tools"]]
    print("MCP handshake: PASS")
    print("Protocol:", init["result"]["protocolVersion"])
    print("Tools:", ", ".join(names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
