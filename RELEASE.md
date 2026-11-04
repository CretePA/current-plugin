# Publishing Current

## Current readiness

The packages target `https://app.current.co/mcp/portal`. On November 2, 2026,
its public portal resource discovery returned HTTP 404, `OAuth is not configured`.
Deploy the shared OAuth configuration update in platform PR #7553, which reuses
the existing MCP issuer and derives the `/mcp/portal` audience. No additional
production variables are required. Then run `python3 scripts/release.py probe` again. A reachable
HTTPS host alone does not establish working OAuth. Do not substitute the staff
MCP resource. Deployment configuration remains owned by platform.

Before submission:

- MIT is selected for the plugin packages. The root license is copied into both
  packages and checked for consistency; it does not license the hosted platform.
- Confirm `support_email`, `privacy_policy_url`, and `walkthrough_url`, then add
  them to `release.json`. Enter them in provider listing forms; these release
  fields are not automatically imported into provider metadata.
- Verify publisher identity and developer account permissions for the agreed
  owners. Complete legal/data-handling attestations with those owners.
- Deploy the portal tool stack. Enable `client-portal-agent` for synthetic reviewer
  identities. Verify all review scenarios on each advertised product surface.
- Provide private reviewer credentials in the provider portal only. OpenAI
  requires a sample-data account without interactive email/SMS codes, magic
  links, or manual MFA approval. Do not weaken normal client authentication.
- Record the walkthrough and results below. These scenarios are planned cases,
  not claims of completed production validation.

## Release procedure

1. Update matching provider manifest versions, shared skill and package README.
   Run `python3 scripts/release.py sync`, then `check` and `build`.
2. Run `claude plugin validate --strict claude` and the installed OpenAI
   plugin-creator validator against `codex/current`. CI checks package
   consistency and archive reproducibility; provider validation is separate.
3. Run `python3 scripts/release.py submission`. This checks license declarations,
   listing fields and public OAuth discovery. It does not certify legal terms,
   reviewer access or authenticated tool execution.
4. OpenAI: upload `dist/current-openai-<version>.zip` at
   https://platform.openai.com/plugins, select the remote MCP path, configure
   OAuth/domain verification, enter review materials, resolve findings and submit.
5. Claude: submit repository `CretePA/current-plugin`, plugin path `claude`,
   using a reviewed release commit/tag at https://claude.ai/directory/manage.
   Submit the hosted MCP separately as a connector. The repo may remain private
   during validation/submission but must be public before listing goes live.
6. Publish only after approval. Configure the portal with verified listing URLs.
   Smoke-test installation from the listing, including revocation and reconnect.

Do not publish a local-marketplace deep link as a universal consumer install link.
A marketplace catalog is useful for private testing but is not public approval.
Keep installation, OAuth consent and successful tool access separate in the UI.

## Reviewer scenarios

Use synthetic clients, returns and documents. Record product/version, date,
expected vs actual result and trace/receipt references for each case. Tool names
may have provider prefixes. Never include credentials in evidence.

| Case | Prompt / setup | Expected tools and result |
| --- | --- | --- |
| Positive 1: discovery | “Which returns can I send documents to?” | `listUploadDestinations`; only this client's authorized destinations; follow pagination. |
| Positive 2: requests | “What is missing for my 2024 Form 1040?” | Discovery then `getDocumentRequests`; report outstanding requests without calling the return complete or reviewed. |
| Positive 3: delivery | Provide a synthetic matching W-2; authorize upload to the selected return | `uploads.begin`, multipart HTTP upload, `listUploadReceipts`; returned file ID matches receipt. |
| Positive 4: retry | Interrupt after successful upload, resume with original idempotency key | Receipts and same-key retry; one stored document, no duplicate submission. |
| Positive 5: reconnect | Revoke Current, reconnect through the host, request outstanding documents again | Old access fails; fresh authorization and read succeed without reinstalling the skill. |
| Negative 1: unauthorized client | Ask for a synthetic client outside the reviewer grant | No data or upload access; never switch identities or guess destination IDs. |
| Negative 2: ambiguous year | Provide destinations for two years and ask “upload my W-2” | Ask which return and confirm files before `uploads.begin`; no silent latest-year choice. |
| Negative 3: unavailable upload capability | Use a surface without file bytes or outbound HTTP | Explain limitation and offer portal upload; no fabricated receipt or claim of delivery. |

Also turn the feature flag off after issuing an upload credential: MCP data
access and credential redemption must fail. Test provider cancellation, expired
auth and a fresh account installation rather than only existing local installs.

## Release notes — 0.1.0

Initial document-collection plugin: discover authorized returns, read document
requests, confirm uploads and verify receipts. Includes one shared skill and a
remote Current portal MCP connection. File submission requires a host with file
access and outbound HTTP; other surfaces use the portal upload fallback.

## Official references

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission
- https://claude.com/docs/plugins/submit
- https://claude.com/docs/plugins/pre-submission-checklist
