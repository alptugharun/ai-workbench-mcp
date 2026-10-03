# Real-host verification

This file records **maintainer-run runtime evidence** separately from package, registry and CI evidence.

It is not an independent third-party endorsement and it is not a claim of universal MCP-host compatibility.

## Verified host run — 2026-10-03

- Host: Cursor 3.20.21
- Server connection name: `ai-workbench-mcp`
- Package line under test: `alptugharun-ai-workbench-mcp==0.1.0a1`
- Transport: stdio
- Result: all three public tools were invoked successfully from the host UI

### 1. Catalog discovery

Tool:

`list_prompts`

Observed result:

- 12 prompts
- 4 assistant blueprints
- returned IDs matched the bundled catalog

This verifies that Cursor connected to the MCP server and received a real tool result rather than a copied README example.

### 2. Prompt rendering

Tool:

`render_prompt`

Prompt ID:

`evidence-brief`

Variables used:

- question: `Should we publish AI Workbench MCP as a public alpha?`
- sources: three supplied source notes
- language: `English`

Observed result:

- the bundled prompt template was rendered with the supplied values
- the result kept the supplied evidence boundary
- no extra source was invented

### 3. Assistant export

Tool:

`get_assistant`

Assistant ID:

`evidence-desk`

Target:

`chatgpt`

Observed result included:

- Status
- Instructions
- Conversation starters
- Acceptance checks

## What this proves

This run is evidence that the published MCP package can be connected to one real Cursor host and that its three public tools can execute through the host.

It complements, but does not replace:

- unit tests
- stdio protocol tests
- clean PyPI installation verification
- official MCP Registry publication
- CI on Linux and Windows

## What this does not prove

It does not prove that:

- every MCP host behaves identically
- every Cursor version is compatible
- another user's machine will have the same environment
- the package is production-ready for every workflow

Independent verification from another user or host is still valuable.

## Reproduce the host checks

After connecting the server, ask the host to perform these checks without answering from memory:

1. Call `list_prompts` and return the catalog result.
2. Call `render_prompt` with a known prompt ID and explicit variables.
3. Call `get_assistant` with a known assistant ID and target.
4. Compare the returned IDs and structure with the repository catalog.
5. Record the host name/version and package version.

A host result should only be marked verified when the tools actually execute and the returned structure is inspected.
