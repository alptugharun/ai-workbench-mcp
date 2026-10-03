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

## Reporting

Do not post exploit details, credentials, or sensitive data in a public issue.

Open a minimal issue stating that you found a security concern and ask for a private contact path, or use GitHub's private vulnerability reporting when it is available for the repository.

A useful report includes the affected commit, reproduction steps, impact, and the smallest known mitigation.

## Maintainer rule

Security fixes should add a regression test when practical and should never weaken validation to make a failing check disappear.
