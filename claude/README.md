# Claude distribution scaffold

This source becomes one `current` plugin: a remote HTTP MCP connector plus the shared `collect-documents` skill. It is not yet a published listing. There is no endpoint or credential embedded in source.

## Build and validate

From the repository root, run with the actual deployed HTTPS portal MCP URL:

```sh
python3 claude/build.py \
  --mcp-url "$PORTAL_MCP_URL" --output /tmp/current-claude-build
claude plugin validate --strict /tmp/current-claude-build/current
```

The output includes a self-contained folder and `current-claude.zip`. The source template is intentionally not installable; the build copies the shared skill as a regular file and resolves the endpoint. A passing CLI validation checks structure, not OAuth or upload behavior. Do not ship a temporary tunnel as the production endpoint.

## Pilot installation

1. In a Claude account that permits plugins, open Customize → Plugins and upload the generated ZIP. Chat, Desktop Chat, and Cowork support account plugins; organization policies may block them.
2. Authorize Current when prompted for its connector. Installation does not grant access on its own. No secret or manually copied access token belongs in the package.
3. Return to Current. Confirm the exact portal MCP OAuth grant is present, then run the document collection example in Claude.
4. Verify request reads, one synthetic upload and receipt, retry without duplication, and revocation. A Chat-only runtime without outbound file upload can read requests but must fall back to the portal for submission.

## Public distribution

Publish the built, self-contained folder to a release branch or folder in this repository. Claude's directory limits repository size and requires a public repository before the listing goes live. Select a license with the owner and add it before submission; this scaffold deliberately does not grant a license. Finalize contact, privacy/data handling details, and public repository metadata.

Submit through <https://claude.ai/directory/manage>: **Plugin bundle**, repository + plugin path, Validate, listing/data handling/compliance, then review. Submit the owned remote MCP server separately as an **MCP connector** too. Configure the production endpoint and OAuth provider for Claude's actual client identity and redirect requirements; don't infer trust from an application display name. Confirm account eligibility, GitHub push access, and provider review requirements before submission.

Once published, store the actual listing URL in Current's connect-agent setup. Until then, offer the ZIP pilot flow; never invent an install URL or call an ordinary app launch an installation.

## Handoff

The documented draft links are `claude://claude.ai/new?q=...` and `claude://cowork/new?q=...` (URL-encode the prompt). Neither installs the plugin, completes OAuth, nor confirms connection. No connector-settings or plugin-install custom-scheme route is documented. Keep a copy-prompt fallback and instructions for users who are signed out, lack the app, lack the required feature, or have installation disabled.

## Official references

- [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Manifest reference](https://code.claude.com/docs/en/plugins-reference)
- [Submit a plugin](https://claude.com/docs/plugins/submit)
- [Directory validation requirements](https://claude.com/docs/plugins/pre-submission-checklist)
- [Organization distribution](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization)
- [Desktop link formats](https://support.claude.com/en/articles/14729294-open-claude-desktop-with-a-link)
