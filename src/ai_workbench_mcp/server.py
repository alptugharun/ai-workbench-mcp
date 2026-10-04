"""Dependency-free stdio MCP server for the packaged AI Workbench catalog."""
from __future__ import annotations

import json
import re
import sys
from importlib.resources import files
from typing import Any

from . import __version__

VERSIONS = ("2025-06-18", "2025-03-26")
LINE_LIMIT = 128000
MAX_INPUT = 32000
PLACEHOLDER_RE = re.compile(r"\{\{([a-z_]+)\}\}")

TOOLS = [
    {
        "name": "list_prompts",
        "description": "List the bundled prompt templates and assistant blueprints available in this local catalog.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {
            "title": "List AI Workbench Catalog",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    },
    {
        "name": "render_prompt",
        "description": "Render one bundled prompt template using supplied string variables. Returns text only and does not call an AI provider.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Prompt ID returned by list_prompts."},
                "variables": {
                    "type": "object",
                    "description": "Exact template variables as non-empty strings.",
                    "additionalProperties": {"type": "string"},
                },
            },
            "required": ["id", "variables"],
            "additionalProperties": False,
        },
        "annotations": {
            "title": "Render Prompt Template",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    },
    {
        "name": "get_assistant",
        "description": "Return one bundled assistant blueprint formatted for a selected host. This does not create, install, publish, or modify an assistant account.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Assistant ID returned by list_prompts."},
                "target": {
                    "type": "string",
                    "enum": ["chatgpt", "claude", "gemini", "grok", "skill"],
                    "description": "Host format for the returned instruction blueprint.",
                },
            },
            "required": ["id", "target"],
            "additionalProperties": False,
        },
        "annotations": {
            "title": "Get Assistant Blueprint",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    },
]


class WorkbenchError(ValueError):
    """A safe, user-actionable local catalog error."""


def load_catalog() -> dict:
    try:
        data = json.loads(files("ai_workbench_mcp").joinpath("catalog.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WorkbenchError("Bundled catalog is unavailable or invalid.") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise WorkbenchError("Unsupported catalog schema.")
    for group in ("prompts", "assistants"):
        entries = data.get(group)
        if not isinstance(entries, list) or not entries:
            raise WorkbenchError(f"Catalog requires a non-empty {group} list.")
    return data


def lookup(catalog: dict, group: str, slug: str) -> dict:
    for entry in catalog[group]:
        if entry.get("id") == slug:
            return entry
    raise WorkbenchError(f"Unknown {group} ID. Call list_prompts first.")


def render_prompt(entry: dict, values: dict) -> str:
    if not isinstance(values, dict):
        raise WorkbenchError("Prompt variables must be an object.")
    required = set(PLACEHOLDER_RE.findall(entry["instructions"]))
    if set(values) != required:
        missing, extra = required - set(values), set(values) - required
        raise WorkbenchError(f"Variable mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
    if any(not isinstance(value, str) or not value.strip() for value in values.values()):
        raise WorkbenchError("Every variable must be a non-empty string.")
    rendered = PLACEHOLDER_RE.sub(lambda match: values[match.group(1)], entry["instructions"])
    if len(rendered) > MAX_INPUT:
        raise WorkbenchError("Rendered prompt exceeds 32000 characters.")
    return rendered


def assistant_markdown(entry: dict, target: str) -> str:
    notes = {
        "chatgpt": "Instruction blueprint only. This response does not create or publish a GPT or ChatGPT plugin.",
        "claude": "Instruction blueprint only. This response does not install a Claude Project, plugin, or skill.",
        "gemini": "Instruction blueprint only. This response does not create a Gem or modify a Gemini account.",
        "grok": "Instruction blueprint only. This response does not deploy a Grok bot or modify an X account.",
        "skill": "Portable Agent Skill source. Inspect and install it only in a host that supports this format.",
    }
    if target not in notes:
        raise WorkbenchError("Unknown assistant target.")
    prefix = ""
    if target == "skill":
        prefix = (
            f'---\\nname: {entry["id"]}\\n'
            f'description: {json.dumps(entry["purpose"], ensure_ascii=False)}\\n'
            "license: MIT\\n---\\n\\n"
        )
    starters = "\\n".join(f"- {item}" for item in entry["starters"])
    checks = "\\n".join(f"- {item}" for item in entry["acceptance"])
    return (
        f'{prefix}# {entry["title"]}\\n\\n{entry["purpose"]}\\n\\n'
        f'## Status\\n\\n{notes[target]}\\n\\n## Instructions\\n\\n{entry["instructions"]}\\n\\n'
        f'## Conversation starters\\n\\n{starters}\\n\\n## Acceptance checks\\n\\n{checks}\\n'
    )


def failure(rpc_id, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": rpc_id, "error": {"code": code, "message": message}}


class CatalogServer:
    def __init__(self, catalog: dict):
        self.catalog = catalog
        self.initialized = False
        self.ready = False

    def call_tool(self, name: str, arguments: Any) -> str:
        if not isinstance(arguments, dict):
            raise WorkbenchError("Tool arguments must be an object.")
        if name == "list_prompts" and not arguments:
            entries = {
                group: [
                    {"id": item["id"], "title": item["title"], "purpose": item["purpose"]}
                    for item in self.catalog[group]
                ]
                for group in ("prompts", "assistants")
            }
            return json.dumps(entries, ensure_ascii=False)
        if name == "render_prompt" and set(arguments) == {"id", "variables"} and isinstance(arguments["id"], str):
            return render_prompt(lookup(self.catalog, "prompts", arguments["id"]), arguments["variables"])
        if (
            name == "get_assistant"
            and set(arguments) == {"id", "target"}
            and isinstance(arguments["id"], str)
            and isinstance(arguments["target"], str)
        ):
            return assistant_markdown(
                lookup(self.catalog, "assistants", arguments["id"]),
                arguments["target"],
            )
        raise WorkbenchError("Unknown tool or invalid arguments.")

    def handle(self, message: Any) -> dict | None:
        if not isinstance(message, dict):
            return failure(None, -32600, "Expected a JSON-RPC object; batches are not supported.")
        rpc_id = message.get("id")
        if message.get("jsonrpc") != "2.0" or not isinstance(message.get("method"), str):
            return failure(None, -32600, "Invalid JSON-RPC request.")
        if "id" in message and type(rpc_id) not in (str, int):
            return failure(None, -32600, "Request ID must be a string or integer.")
        method = message["method"]
        if "id" not in message:
            if method == "notifications/initialized" and self.initialized:
                self.ready = True
            return None
        params = message.get("params", {})
        if not isinstance(params, dict):
            return failure(rpc_id, -32602, "params must be an object.")
        if method == "initialize":
            if self.initialized:
                return failure(rpc_id, -32600, "Already initialized.")
            if not isinstance(params.get("protocolVersion"), str):
                return failure(rpc_id, -32602, "protocolVersion is required.")
            requested = params["protocolVersion"]
            version = requested if requested in VERSIONS else VERSIONS[0]
            self.initialized = True
            result = {
                "protocolVersion": version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "alptugharun-ai-workbench-mcp", "version": __version__},
            }
        elif method == "ping":
            result = {}
        elif not self.ready:
            return failure(rpc_id, -32600, "Complete initialization before using catalog tools.")
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            if not isinstance(params.get("name"), str):
                return failure(rpc_id, -32602, "Tool name is required.")
            try:
                text = self.call_tool(params["name"], params.get("arguments", {}))
                result = {"content": [{"type": "text", "text": text}], "isError": False}
            except WorkbenchError as exc:
                result = {"content": [{"type": "text", "text": str(exc)}], "isError": True}
        else:
            return failure(rpc_id, -32601, "Method not supported by this read-only server.")
        return {"jsonrpc": "2.0", "id": rpc_id, "result": result}


def serve(input_stream, output_stream, catalog: dict) -> int:
    server = CatalogServer(catalog)
    while True:
        line = input_stream.readline(LINE_LIMIT + 1)
        if not line:
            return 0
        if len(line) > LINE_LIMIT:
            print(
                json.dumps(failure(None, -32600, "Request line exceeds limit; closing transport.")),
                file=output_stream,
                flush=True,
            )
            return 2
        if not line.strip():
            continue
        try:
            response = server.handle(json.loads(line))
        except json.JSONDecodeError:
            response = failure(None, -32700, "Invalid JSON.")
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), file=output_stream, flush=True)


def doctor_payload() -> dict:
    """Return local, side-effect-free diagnostics for first-run support."""
    catalog = load_catalog()
    return {
        "status": "pass",
        "package_version": __version__,
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "supported_protocols": list(VERSIONS),
        "tools": [tool["name"] for tool in TOOLS],
        "catalog": {
            "prompts": len(catalog["prompts"]),
            "assistants": len(catalog["assistants"]),
        },
        "boundaries": {
            "network": False,
            "shell": False,
            "filesystem_write": False,
            "account_access": False,
        },
        "next_step": "Configure a stdio MCP host, then call list_prompts.",
    }


def main() -> int:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    args = sys.argv[1:]
    if args:
        if args == ["--version"]:
            print(__version__)
            return 0
        if args == ["--doctor"]:
            try:
                print(json.dumps(doctor_payload(), ensure_ascii=False, indent=2))
                return 0
            except (WorkbenchError, OSError, UnicodeError):
                print(
                    json.dumps(
                        {
                            "status": "fail",
                            "error": "Bundled catalog is unavailable or invalid.",
                            "next_step": "Reinstall the exact published package in a clean environment.",
                        }
                    )
                )
                return 2
        print("Usage: alptugharun-ai-workbench-mcp [--doctor|--version]", file=sys.stderr)
        return 2

    try:
        return serve(sys.stdin, sys.stdout, load_catalog())
    except (WorkbenchError, OSError, UnicodeError):
        print("Cannot load the bundled catalog; no tools started.", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
