# Contributing

Thanks for helping improve AI Workbench MCP.

## Before you start

Keep changes small and testable. This repository intentionally avoids turning a read-only local catalog into a broad agent framework.

Good contributions include:

- protocol edge-case tests;
- host compatibility reports;
- clearer error handling;
- documentation fixes;
- catalog corrections;
- packaging and release hardening.

## Local checks

```bash
python -m unittest discover -s tests -v
python examples/smoke_client.py
```

If a test could not run, say so in the pull request.

## Pull requests

Explain:

- what changed;
- why it matters;
- how you tested it;
- whether permissions, network access, package metadata, or tool behavior changed.

Do not weaken tests or broaden permissions just to make a check pass.

## Security

Do not include tokens, cookies, API keys, private prompts, private account data, or confidential files in issues or PRs.

For security concerns, follow [SECURITY.md](SECURITY.md).
