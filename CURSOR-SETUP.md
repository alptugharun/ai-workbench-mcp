# Cursor setup — AI Workbench MCP

This guide turns the published `alptugharun-ai-workbench-mcp==0.1.0a1` package into a working local stdio MCP server in Cursor.

Verified maintainer evidence currently covers Cursor 3.20.21. Host behavior can change, so keep the package/host version with any bug report.

## What you get

After setup, Cursor should discover three read-only tools:

- `list_prompts`
- `render_prompt`
- `get_assistant`

The server does not request network access, shell execution, account access, filesystem writes, or provider API access.

## 1. Check Python

Python 3.10 or newer is required.

```bash
python --version
```

If `python` points to the wrong interpreter, use the command your machine normally uses for Python 3.

## 2. Install the exact published version

```bash
python -m pip install "alptugharun-ai-workbench-mcp==0.1.0a1"
```

Confirm that the same Python interpreter can import it:

```bash
python -c "import ai_workbench_mcp; print(ai_workbench_mcp.__version__)"
```

Expected output:

```text
0.1.0a1
```

## 3. Add the Cursor MCP configuration

Cursor supports project-specific configuration at:

```text
.cursor/mcp.json
```

and global configuration at:

```text
~/.cursor/mcp.json
```

Use the checked-in example from [examples/cursor-mcp.json](examples/cursor-mcp.json):

```json
{
  "mcpServers": {
    "ai-workbench-mcp": {
      "type": "stdio",
      "command": "python",
      "args": [
        "-m",
        "ai_workbench_mcp.server"
      ]
    }
  }
}
```

The important rule is that the `python` command Cursor launches must be the same environment where you installed the package.

### If Cursor uses a different Python

Find the interpreter used for installation:

```bash
python -c "import sys; print(sys.executable)"
```

Then replace `"command": "python"` with that absolute executable path.

Windows JSON paths need escaped backslashes, for example:

```json
{
  "mcpServers": {
    "ai-workbench-mcp": {
      "type": "stdio",
      "command": "C:\\Path\\To\\python.exe",
      "args": [
        "-m",
        "ai_workbench_mcp.server"
      ]
    }
  }
}
```

## 4. Confirm Cursor sees the server

Open Cursor's MCP settings / Customize surface and confirm that `ai-workbench-mcp` is connected.

If you use Cursor CLI, current Cursor documentation also provides:

```bash
agent mcp list
agent mcp list-tools ai-workbench-mcp
```

The tool list should contain exactly:

```text
list_prompts
render_prompt
get_assistant
```

## 5. Run the three host-level checks

Do not accept a green connection badge as the final proof. Invoke the tools.

### Check A — catalog

Ask Cursor:

```text
Use the MCP server ai-workbench-mcp. Call list_prompts. Return only the tool result.
```

Expected evidence:

- prompt entries are returned;
- assistant entries are returned;
- current bundled catalog contains 12 prompts and 4 assistants.

### Check B — prompt rendering

Ask Cursor:

```text
Use the MCP server ai-workbench-mcp. Call render_prompt with prompt ID evidence-brief.
Use question = Should we publish this as a public alpha?
Use sources = S1: The package is installed. S2: The host called list_prompts successfully.
Use language = English.
Do not invent evidence. Return only the rendered prompt.
```

Expected evidence:

- the request invokes `render_prompt`;
- supplied variables appear in the rendered prompt;
- no new source is invented.

### Check C — assistant export

Ask Cursor:

```text
Use the MCP server ai-workbench-mcp. Call get_assistant with assistant ID evidence-desk and target chatgpt. Do not answer from memory. Return only the tool result.
```

Expected evidence includes:

- Status
- Instructions
- Conversation starters
- Acceptance checks

## Troubleshooting

### Cursor says the server is disconnected

First confirm the configured interpreter can import the package:

```bash
python -c "import ai_workbench_mcp; print(ai_workbench_mcp.__version__)"
```

If that fails, install the package into that interpreter or point `command` to the interpreter where the package is already installed.

### `alptugharun-ai-workbench-mcp` is not found

The console-script directory may not be on PATH. The recommended Cursor config in this guide avoids that problem by launching:

```text
python -m ai_workbench_mcp.server
```

### The process appears to do nothing in a terminal

That can be normal. This is an stdio MCP server: it waits for MCP JSON-RPC input on stdin. Use the repository smoke client or connect through an MCP host instead of expecting a normal interactive shell UI.

### Cursor connects but a tool call fails

Record:

- Cursor version;
- package version;
- Python executable;
- tool name;
- exact arguments;
- expected result;
- returned error.

Do not call a host “verified” when only connection succeeded.

## Repository-level verification

If you cloned this repository:

```bash
python -m unittest discover -s tests -v
python examples/smoke_client.py
```

These tests verify the package/protocol behavior. They complement, but do not replace, the Cursor host calls above.

## Uninstall

Remove the `ai-workbench-mcp` entry from the relevant Cursor `mcp.json`, then uninstall the Python package:

```bash
python -m pip uninstall alptugharun-ai-workbench-mcp
```

## Evidence boundary

A successful Cursor run proves that one named host/version can invoke the tools in that environment. It does not prove compatibility with every MCP client.

See [HOST-VERIFICATION.md](HOST-VERIFICATION.md) for the dated maintainer-run result.
