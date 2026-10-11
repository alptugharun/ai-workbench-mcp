# AI Workbench MCP — Beginner Guide

If you have never used MCP before, start here.

You do not need to understand the full Model Context Protocol specification to use this server.

The shortest mental model is:

**your AI host → asks a named tool to do one local catalog job → AI Workbench MCP returns text**

This server is intentionally small and read-only.

---

## 1. What is an MCP server?

An MCP server exposes structured tools/resources to a compatible AI host.

Instead of telling the model:

> “Please somehow read this local catalog…”

the host can see explicit tools with names, input schemas and permission hints.

AI Workbench MCP exposes only three tools.

| Tool | Use it when… | Result |
| --- | --- | --- |
| `list_prompts` | you do not yet know the valid prompt/assistant IDs | catalog metadata |
| `render_prompt` | you want one prompt template filled with your variables | plain prompt text |
| `get_assistant` | you want one reusable assistant blueprint formatted for a host | Markdown blueprint |

---

## 2. What does this server NOT do?

It does not:

- browse the web;
- call OpenAI, Claude, Gemini or Grok;
- execute shell commands;
- write or delete files;
- sign into accounts;
- publish content;
- read browser cookies or credentials.

That is the point.

The project demonstrates a **small MCP permission boundary** that is easy to inspect.

---

## 3. Requirements

You need:

- Python 3.10 or newer;
- a terminal;
- later, an MCP-compatible host if you want real host use.

You do **not** need an API key for the local package/doctor test.

---

## 4. Install the exact published alpha

```bash
python -m pip install "alptugharun-ai-workbench-mcp==0.1.0a2"
```

If you use multiple Python environments, make sure this command runs in the same environment that your MCP host will launch.

---

## 5. First test: doctor

Before editing any host configuration, run:

```bash
alptugharun-ai-workbench-mcp --doctor
```

A healthy result is JSON and includes:

- `"status": "pass"`;
- package version;
- Python version;
- all three public tool names;
- prompt/assistant counts;
- the local permission boundary.

### What doctor proves

It proves the installed package can load its bundled catalog.

### What doctor does NOT prove

It does not prove:

- Cursor/Claude/another host is configured correctly;
- every MCP client supports the same config format;
- an independent third party has verified your environment.

---

## 6. Understand the three tools

### Step A — call list_prompts first

Use this when you need valid IDs.

Conceptually:

```text
list_prompts()
```

You get prompt and assistant entries with IDs/titles/purpose.

Do this before guessing an ID.

### Step B — render a prompt

Use `render_prompt` when you want **one prompt template turned into final text**.

It needs:

- prompt `id`;
- the exact required `variables`.

If a variable is missing or extra, the server rejects the request instead of silently producing ambiguous output.

Use `get_assistant` instead when you want a reusable assistant configuration.

### Step C — get an assistant blueprint

Use `get_assistant` when you want **one assistant job formatted for a target host**.

Targets currently include:

- ChatGPT;
- Claude;
- Gemini;
- Grok;
- portable Agent Skill format.

This returns instruction text/Markdown.

It does **not** create or publish the assistant in your account.

Use `render_prompt` instead when the job is a single filled prompt.

---

## 7. Connect a real MCP host

The host we have actually exercised is Cursor.

Use:

- `CURSOR-SETUP.md`
- `HOST-VERIFICATION.md`

Do not copy Cursor configuration into another MCP client and assume it is universal.

Each host may use different config locations/fields.

---

## 8. The verification ladder

Always verify in this order:

1. **installed**
2. **doctor pass**
3. **MCP handshake**
4. **host discovers all 3 tools**
5. **tool invocation succeeds**
6. **output matches the documented job**

One level does not automatically prove the next.

---

## 9. Troubleshooting

Use `TROUBLESHOOTING.md`.

Common problems:

### Command not found

Your package may be installed in a different Python environment/PATH.

### Host connects but tools do not appear

Connection and tool discovery are separate.

Reload the host and verify the launch command.

### Unknown ID

Call `list_prompts` first.

### Prompt variable mismatch

Use the exact variables required by the catalog entry.

### Windows / WSL confusion

Install and run on the same side of the Windows/WSL boundary that your MCP host launches.

---

## 10. Security model

Every tool declares:

```json
{
  "readOnlyHint": true,
  "destructiveHint": false,
  "idempotentHint": true,
  "openWorldHint": false
}
```

The code is also tested to avoid importing network/process modules in the server path.

That is evidence about **this implementation**.

It is not a reason to trust arbitrary MCP servers.

---

## 11. Package and registry

The package is published on PyPI.

The official MCP Registry entry is:

`io.github.alptugharun/ai-workbench-mcp`

The Registry verifies standardized publication identity/metadata. It is not a universal security certificate.

The release workflow uses GitHub OIDC Trusted Publishing and Sigstore signing.

---

## 12. What should I try first?

If you only want to see the concept:

1. install;
2. run `--doctor`;
3. read the three tool descriptions.

If you want a real host test:

1. doctor;
2. Cursor setup;
3. call `list_prompts`;
4. render one prompt;
5. get one assistant blueprint;
6. report PASS/FAIL/BLOCKED with environment details.

---

## 13. When should I NOT use this server?

Do not use it when you need:

- web research;
- filesystem editing;
- social publishing;
- account management;
- an AI model call;
- a broad autonomous agent.

The server intentionally does not have those powers.

Use the smallest boundary that solves the job.
