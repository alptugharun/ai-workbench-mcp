# Official MCP Registry Publishing Gate

This repository is the standalone distribution boundary for the read-only AI Workbench MCP server.

## Planned identity

- MCP server name: `io.github.alptugharun/ai-workbench-mcp`
- PyPI package: `alptugharun-ai-workbench-mcp`
- transport: `stdio`
- runtime hint: `uvx`
- first package candidate: `0.1.0a1`
- release tag: `v0.1.0a1`

The README contains the ownership marker:

```text
mcp-name: io.github.alptugharun/ai-workbench-mcp
```

## Current verified state — 2026-10-03

- PyPI version `0.1.0a1` is published through GitHub OIDC Trusted Publishing.
- The release workflow publishes the wheel before generating Sigstore bundles, preventing signature metadata from being mistaken for a Python distribution.
- A clean exact-version install from PyPI succeeded.
- stdio verification passed for initialize, notifications/initialized, tools/list, successful render_prompt, successful get_assistant, and a bounded unknown-tool error.
- `server.json` validates successfully against the production MCP Registry using `mcp-publisher v1.8.1`.
- Real-host compatibility evidence is still tracked separately from package/registry validation.

## Pre-publish checks

```bash
python -m unittest discover -s tests -v
python -m pip wheel --no-deps . --wheel-dir dist
python -m pip install --no-deps --force-reinstall dist/*.whl
python examples/smoke_client.py
```

## PyPI Trusted Publisher

This repo is designed for GitHub OIDC Trusted Publishing. Do not store a long-lived PyPI token in repository secrets.

Pending publisher values:

- project: `alptugharun-ai-workbench-mcp`
- owner: `alptugharun`
- repository: `ai-workbench-mcp`
- workflow: `publish-pypi.yml`
- environment: `pypi`

## Publication order

1. [x] all CI checks pass on the release commit;
2. [x] GitHub release `v0.1.0a1` is published;
3. [x] GitHub OIDC publishes the wheel to PyPI;
4. [x] Sigstore signs the published release artifacts;
5. [x] install the exact version in a clean environment;
6. [x] verify initialize → initialized → tools/list → public tools/call paths and bounded invalid-tool behavior;
7. [x] add `server.json` using the current schema;
8. [x] run `mcp-publisher validate server.json`;
9. [ ] publish to the official MCP Registry through GitHub OIDC;
10. [ ] record at least one real-host result separately from registry acceptance.

Registry acceptance is metadata/ownership evidence, not universal host compatibility.
