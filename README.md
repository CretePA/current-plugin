# Current plugins

Codex and Claude packages for collecting an accountant's requested documents.
Both bundle the same [skill](shared/skills/collect-documents/SKILL.md) and a remote
portal MCP connection. The server, OAuth, permissions, and portal UI live in
[platform](https://github.com/CretePA/platform).

## Build

Use Python 3, a deployed HTTPS `/mcp/portal` endpoint, and new output directories:

```sh
python3 codex/build.py --mcp-url "$PORTAL_MCP_URL" --output dist/codex/current
python3 claude/build.py --mcp-url "$PORTAL_MCP_URL" --output dist/claude
claude plugin validate --strict dist/claude/current
```

Codex produces a self-contained `current` folder; Claude also produces
`dist/claude/current-claude.zip`. Both copy the shared skill. Install the built
artifact, authorize Current, and verify a fresh tool call. Rebuild after edits.
Use Codex's plugin-creator validator for its built folder.

## Release

Source templates are not installable packages. Claude directory submission must
point at a committed **built folder**, including its skill and MCP configuration.
Do not point a client install button at this source repository as if it were a
published plugin listing; configure verified provider install links separately.

Before public distribution: stable endpoint, publisher/privacy/support metadata,
license decision, and provider approval. Keep credentials and customer data out
of packages. This repository is private; neither plugin is publicly listed.

Verify install → authorize → read requests → confirm upload → verify receipt →
revoke → reconnect. Installation, authorization, and a successful tool call are
separate checks. A host without file/network access must use portal upload.
