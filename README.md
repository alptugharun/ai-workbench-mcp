# AI Workbench MCP

[![CI](https://github.com/alptugharun/ai-workbench-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/alptugharun/ai-workbench-mcp/actions/workflows/ci.yml)
[![CodeQL](https://github.com/alptugharun/ai-workbench-mcp/actions/workflows/codeql.yml/badge.svg)](https://github.com/alptugharun/ai-workbench-mcp/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/alptugharun/ai-workbench-mcp/badge)](https://scorecard.dev/viewer/?uri=github.com/alptugharun/ai-workbench-mcp)
[![PyPI](https://img.shields.io/pypi/v/alptugharun-ai-workbench-mcp?include_prereleases&label=PyPI)](https://pypi.org/project/alptugharun-ai-workbench-mcp/)

<!-- mcp-name: io.github.alptugharun/ai-workbench-mcp -->

[![English](https://img.shields.io/badge/English-0D1117?style=flat-square)](README.md) [![Türkçe](https://img.shields.io/badge/Türkçe-E30A17?style=flat-square)](README_TR.md)

<p align="center">
  <strong>A tiny, read-only MCP server for reusable AI prompts and assistant blueprints.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/MCP-read--only-111827?style=for-the-badge" alt="MCP read-only">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/runtime-dependency--free-16A34A?style=for-the-badge" alt="Dependency-free runtime">
  <img src="https://img.shields.io/badge/license-MIT-2563EB?style=for-the-badge" alt="MIT">
</p>

AI Workbench MCP exposes a small local catalog over **Model Context Protocol stdio**. It is intentionally boring in the best way: no network calls, no shell execution, no account access, no file writes, no hidden provider request.

It gives an MCP host three tools:

| Tool | Result |
| --- | --- |
| `list_prompts` | Lists the bundled prompt templates and assistant blueprints |
| `render_prompt` | Fills a bundled prompt template with explicit string variables |
| `get_assistant` | Returns one assistant blueprint for ChatGPT, Claude, Gemini, Grok, or portable Agent Skill format |

## Why this exists

A lot of AI repos jump straight from "here is a prompt" to "this is an agent." I wanted a smaller boundary that is easy to inspect.

The server keeps the useful parts local and makes its limits obvious:

- **read-only** tool contracts;
- explicit MCP trust hints;
- bounded input sizes;
- strict top-level schemas;
- no runtime dependencies outside the Python standard library;
- real stdio handshake tests;
- named tests for every public tool.

## Quick start

Install the published alpha package:

```bash
python -m pip install "alptugharun-ai-workbench-mcp==0.1.0a1"
```

Confirm the local package can load before touching host configuration:

```bash
alptugharun-ai-workbench-mcp --doctor
```

A healthy result reports the package/Python versions, all three tool names, catalog counts and the read-only permission boundary. It makes no network request and does not prove host compatibility; it tells you whether the **local package layer** is healthy.

Then point a stdio-capable MCP host at the server:

Launch command:

```text
alptugharun-ai-workbench-mcp
```

This repository documents the stdio server itself. For the host we have actually exercised, use the copy/paste [Cursor setup and 3-tool verification guide](CURSOR-SETUP.md). Other MCP clients can differ, so use their current documentation rather than assuming Cursor's configuration is portable.

## Security model

Every public tool declares:

```json
{
  "readOnlyHint": true,
  "destructiveHint": false,
  "idempotentHint": true,
  "openWorldHint": false
}
```

The implementation does not import HTTP clients, subprocess modules, filesystem-write helpers, browser libraries, or provider SDKs.

That does **not** mean "trust any MCP server." It means this repository keeps its own boundary narrow and testable.

## Verify it yourself

```bash
python -m unittest discover -s tests -v
python examples/smoke_client.py
```

CI runs the package and protocol tests on Linux and Windows.

## Package / registry status

**PyPI:** `alptugharun-ai-workbench-mcp==0.1.0a1` is published through GitHub OIDC Trusted Publishing. The release workflow also signs the wheel with keyless Sigstore.

A clean Windows virtual environment installed the exact PyPI version successfully, negotiated MCP protocol `2025-06-18`, listed all three tools, completed successful `render_prompt` and `get_assistant` calls, and returned a bounded error for an unknown tool.

**Official MCP Registry:** `io.github.alptugharun/ai-workbench-mcp` is published and currently reports `active` in the production registry.

**Real-host verification:** a maintainer-run Cursor 3.20.21 session invoked `list_prompts`, `render_prompt` and `get_assistant` successfully against the published package. This is host evidence, not an independent third-party endorsement or a universal compatibility claim.

See [REGISTRY-PUBLISHING.md](REGISTRY-PUBLISHING.md), [HOST-VERIFICATION.md](HOST-VERIFICATION.md) and the failure-first [Troubleshooting ladder](TROUBLESHOOTING.md).

## Contributing

Small, reproducible improvements are welcome. The most useful contributions right now are:

- real MCP host verification;
- protocol edge-case tests;
- clearer failure messages;
- documentation corrections;
- narrowly scoped catalog improvements.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR. If the server works in a host we have not independently verified yet, a reproducible host report is more valuable than a generic “works for me.”

## Origin

This project was extracted from [AI Social Media Toolkit](https://github.com/alptugharun/ai-social-media-toolkit) so the MCP server can evolve as a focused product instead of being buried inside a larger creator/AI repository.

Built by **Alptuğ Harun**.

If the server gives you a useful first result, starring the repository helps other MCP users discover it. If it fails, open a reproducible report instead — failures with environment details improve the project faster than vanity metrics.

## License

MIT — see [LICENSE](LICENSE).
