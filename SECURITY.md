# Security Policy

AI Workbench MCP is designed as a local, read-only stdio server.

## Intended boundary

The public tools should not:

- access the network;
- execute shell commands;
- modify files;
- access credentials or browser data;
- sign in to accounts;
- call an AI provider;
- publish external content.

A violation of this boundary, a way to bypass input limits/schema checks, dependency/release compromise, credential exposure, or unsafe MCP protocol behavior should be treated as a potential **vulnerability**.

## Private vulnerability reporting

Do **not** post exploit details, credentials, proof-of-concept secrets, private prompts or sensitive data in a public issue.

Use GitHub Private Vulnerability Reporting:

https://github.com/alptugharun/ai-workbench-mcp/security/advisories/new

A useful report includes:

- affected version and commit when known;
- operating system / Python / MCP host when relevant;
- minimal reproduction steps;
- security impact;
- sanitized logs/output;
- the smallest known mitigation if you have one.

## Coordinated disclosure

The maintainer aims to acknowledge a private vulnerability report within **7 days**.

When a vulnerability is confirmed, the preferred process is coordinated disclosure after a fix or mitigation is available. A **90-day** remediation/disclosure target is a goal for ordinary cases, not a guarantee; severity, ecosystem coordination and reporter agreement may require a shorter or longer timeline.

Please do not publicly disclose an unpatched vulnerability before coordination unless there is an overriding safety reason.

## Maintainer rule

Security fixes should add a regression test when practical and must never weaken validation, permissions or evidence boundaries merely to make a failing check disappear.

This policy describes the reporting process; it is not a claim that the project is vulnerability-free.
