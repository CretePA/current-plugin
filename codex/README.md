# Current for Codex

The plugin packages the restricted portal MCP connection and the shared
`collect-documents` skill. Repository source lives here; generated packages and
local installations are separate copies.

## Build and validate

Run from the repository root with the deployed portal MCP endpoint:

```sh
python3 codex/build.py \
  --mcp-url "$PORTAL_MCP_URL" --output /tmp/current-codex-release/current
```

The new `current` directory contains `.codex-plugin/plugin.json`, `.mcp.json`,
and the skill. Validate the output with Codex's plugin-creator `validate_plugin.py`.
The source template is not installable until the builder supplies the endpoint.

Codex discovers OAuth configuration from the MCP server and registers its client
through the provider flow. Configure Current's trusted Codex client identification
from that actual registration; never infer identity from an application name.
No client secret or access token belongs in this package.

## Install and reconnect

For a local pilot, register the built folder in a personal Codex marketplace and
install Current. Finish sign-in and consent, then verify a fresh Current tool read.
Rebuild and reinstall after source changes; an existing installation does not read
this repository's skill directly. Start a new conversation to pick up changed tools.

Installation and authorization are separate. After revocation, reconnect Current
through Codex's plugin settings; do not require reinstallation. Verify recovery with
a fresh tool read. A portal grant alone does not establish that a conversation has
loaded the tools. Automatic reconnect behavior still requires host verification.

Public distribution needs a stable endpoint, approved publisher metadata, and a
real published listing URL. Temporary tunnels and personal marketplace links are
pilot-only. This package targets Codex; it does not establish ChatGPT compatibility
or a shared OAuth grant.

## Verification

Use a synthetic client to install, authorize, read requests, confirm an upload,
verify its receipt, revoke access, and reconnect without reinstalling. Also check
canceled consent and missing tools. Package validation checks structure only.
Uploading requires file access and an outbound HTTP runtime; otherwise the skill
routes the client to portal upload.

[Codex plugin packaging documentation](https://developers.openai.com/plugins/build/plugins)
