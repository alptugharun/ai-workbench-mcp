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

## Why server.json is not committed yet

A registry manifest that points at an unpublished package would be misleading. Add `server.json` only after the exact PyPI version exists and a clean install succeeds.

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

1. all CI checks pass on the release commit;
2. GitHub release `v0.1.0a1` is published;
3. the publish workflow builds, inspects and signs one wheel;
4. GitHub OIDC publishes it to PyPI;
5. install the exact version in a clean environment;
6. verify initialize → initialized → tools/list → all three tools/call paths;
7. generate `server.json` with the current `mcp-publisher` CLI;
8. run `mcp-publisher validate server.json`;
9. publish to the official MCP Registry;
10. record at least one real-host result separately from registry acceptance.

Registry acceptance is metadata/ownership evidence, not universal host compatibility.
