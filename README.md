# Current plugins

One workflow: understand outstanding document requests, find files in sources the
client authorizes, confirm the upload, and verify delivery. Each plugin packages
the restricted portal MCP and the same [collect-documents skill](shared/skills/collect-documents/SKILL.md).
Current enforces access; the skill does not grant it.

| Provider | Source | Build output |
| --- | --- | --- |
| Codex | [Codex package](codex/README.md) | Self-contained `current` plugin folder |
| Claude | [Claude package](claude/README.md) | Self-contained folder and plugin ZIP |

Run from the repository root with a deployed HTTPS portal endpoint and new output
directories:

```sh
python3 codex/build.py \
  --mcp-url "$PORTAL_MCP_URL" --output /tmp/current-codex-release/current
python3 claude/build.py \
  --mcp-url "$PORTAL_MCP_URL" --output /tmp/current-claude-release
claude plugin validate --strict /tmp/current-claude-release/current
```

Builders copy the shared skill into each artifact. Rebuild and reinstall after
changing the source. Never package credentials, customer data, or a temporary
tunnel in a public release. Neither plugin is a published listing yet.

Installation, OAuth authorization, and a successful tool call are distinct checks.
Verify each host with a synthetic client: install → authorize → read requests →
confirmed upload → verify receipt → revoke → reconnect → fresh read. A runtime
without file/network access must use portal upload for file submission.

Public release requires a stable endpoint, exact OAuth resource and verified
provider identity, approved distribution metadata, and real listing URLs. Keep
provider-specific setup instructions with each package. Portal UX and rollout are
separate from artifact packaging.

## Ownership and release status

This repository owns plugin manifests, builders, and the shared document-collection
skill. The MCP server, authentication, permissions, and portal UI remain in
[CretePA/platform](https://github.com/CretePA/platform).

Imported from platform commit `ed2c879b9ea974aa6419668c25c1e376cd30511a`,
under `integrations/personal-agents/`. Only plugin files were transferred.

These are source templates: build them before installation. Claude directory
submission must point at the built self-contained folder, not `claude/` here,
because the shared skill and endpoint are materialized by the builder.

The repository is private during preparation. Before public distribution, choose
a license with the owner, finalize publisher/privacy/support metadata, and deploy
a stable MCP endpoint. No open-source license is granted by this scaffold.
Neither package is approved or publicly listed.
