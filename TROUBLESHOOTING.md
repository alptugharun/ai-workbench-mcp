# Troubleshooting

Start with evidence, not guesses.

## 30-second diagnosis

Run the installed package directly:

```bash
alptugharun-ai-workbench-mcp --doctor
```

A healthy local package returns JSON with:

- `"status": "pass"`;
- the installed package version;
- the Python version;
- the three public tool names;
- prompt/assistant counts;
- the local permission boundary.

This command does **not** connect to a host, make a network request, execute a shell command, write files or access an account. A passing doctor result proves the local package/catalog can load. It does **not** prove Cursor, Claude, ChatGPT or another MCP host is configured correctly.

## Failure ladder

Use the first failing layer. Do not skip ahead.

| Layer | Check | If it fails |
| --- | --- | --- |
| 1. Python | `python --version` | Use Python 3.10+ in the same environment that will run the MCP command. |
| 2. Package | `python -m pip show alptugharun-ai-workbench-mcp` | Reinstall the exact published version in a clean environment. |
| 3. Local catalog | `alptugharun-ai-workbench-mcp --doctor` | Reinstall; if it still fails, report Python/OS/package version and the sanitized output. |
| 4. MCP handshake | `python examples/smoke_client.py` from a source checkout | Compare the local protocol result with the host configuration. |
| 5. Host discovery | Confirm the host lists `list_prompts`, `render_prompt`, `get_assistant` | Fix the host command/path/config; a green doctor result alone does not prove discovery. |
| 6. Tool invocation | Call `list_prompts` first | Capture the host error and verify it is calling this server, not a same-named config. |
| 7. Output | Run the documented render/get-assistant examples | Report the exact public tool name, safe inputs and sanitized result. |

## Common failures

### “Command not found”

The package may be installed into a different Python environment or its scripts directory may not be on `PATH`.

Check:

```bash
python -m pip show alptugharun-ai-workbench-mcp
python -m pip --version
```

On Windows PowerShell, also try:

```powershell
py -m pip show alptugharun-ai-workbench-mcp
Get-Command alptugharun-ai-workbench-mcp -ErrorAction SilentlyContinue
```

If `pip show` succeeds but `Get-Command` does not, the problem is command discovery/PATH, not MCP protocol behavior.

### Host says “connected” but no tools appear

Treat **transport connection** and **tool discovery** as separate checks.

1. Run `--doctor`.
2. Confirm the host launch command is exactly `alptugharun-ai-workbench-mcp`.
3. Restart/reload the MCP host after editing its configuration.
4. Confirm the host exposes all three public tools.
5. Call `list_prompts`.

For the host we have actually exercised, use [CURSOR-SETUP.md](CURSOR-SETUP.md).

### Unknown tool / invalid arguments

The server intentionally rejects undeclared tools and extra top-level arguments.

Call `list_prompts` first, then use the exact public schemas returned by `tools/list`. This server has no shell, browser, filesystem-write or account-management tool.

### Prompt variable mismatch

`render_prompt` requires the exact variable set for that prompt. Missing and extra variables are rejected instead of being silently ignored.

Use `list_prompts`, choose a prompt ID, then follow the example in the repository documentation.

### Windows / WSL confusion

Install and run the package in the **same environment** your MCP host launches.

A package installed in WSL is not automatically available to a Windows-native host, and a Windows console script is not automatically available inside WSL.

Verify the environment with:

```bash
python -m pip --version
python -m pip show alptugharun-ai-workbench-mcp
alptugharun-ai-workbench-mcp --doctor
```

Run those commands from the same side of the Windows/WSL boundary as the host command.

## What to include in a bug report

Please include only public-safe diagnostics:

- OS and version;
- Python version;
- package version;
- install command;
- `--doctor` output;
- MCP host and host version;
- whether the host discovered all three tool names;
- exact public tool name that failed;
- sanitized error text.

Do **not** post tokens, cookies, account IDs, private paths, private prompts or confidential documents.

## Verification levels

A successful check at one layer does not silently upgrade the next layer.

**installed → doctor pass → protocol handshake → host discovery → tool invocation → expected output**

That distinction is deliberate. It makes “works on my machine” easier to debug and harder to overclaim.
