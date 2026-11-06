# Publishing Current

## Current readiness

The packages target `https://app.current.co/mcp/portal`. On November 5, 2026,
public OAuth discovery and the unauthenticated 401 challenge passed. Real Codex
OAuth, document discovery, upload, receipt verification and same-key retry passed
against a synthetic production client. Claude connected and read requests, but
its personal-account sandbox could not reach the upload endpoint. ChatGPT and
Claude Team/Enterprise upload have not been verified.

Submission is not ready until the following are complete:

- Confirm a monitored `support_email` and record the walkthrough URL in
  `release.json`. The public privacy policy is configured. Enter these fields
  in provider listing forms; they are not automatically imported into metadata.
- Create a dedicated synthetic reviewer login. Production WorkOS currently has
  Magic Auth enabled and email/password disabled. OpenAI requires reviewers to
  sign in without email/SMS codes, magic links or manual MFA. Agree on a supported
  reviewer authentication approach before changing production configuration;
  do not bypass authentication or disable protections for existing clients.
- Scope that identity to synthetic client data and enable `client-portal-agent`
  for that identity only. Keep credentials out of this repo and provide them
  privately in the provider portal.
- Complete the remaining scenario checks and the recording below. In particular,
  revocation did not immediately invalidate a cached access token; rejection at
  token expiry is still unverified. Reconnection itself worked.
- Verify publisher identity and account permissions. Have the responsible owners
  complete legal and data-handling attestations. MIT covers these packages, not
  the hosted platform.

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

### Production evidence — November 5, 2026

These results used a synthetic production client through Codex CLI 0.166.0 and
personal Claude. They are not proof that every advertised host supports uploads.

| Case | Observed result |
| --- | --- |
| Positive 1 | Codex and Claude returned the synthetic client’s general destination and 2024/2025 returns. |
| Positive 2 | Both read the selected return’s document requests. |
| Positive 3 | Codex uploaded the synthetic W-2; receipt and accountant UI agreed on the 2024 destination. Stored-byte checksum comparison remains unverified. |
| Positive 4 | Same-key retry returned the same file ID and one receipt. |
| Positive 5 | Both reconnected. Codex read requests afterward; Claude showed the connected tool catalog. Cached Codex access still worked after portal revocation; expiry rejection remains unverified. |
| Negative 1 | Codex stopped when the synthetic unavailable client was absent from authorized destinations. This tests agent behavior, not a direct unauthorized-ID backend request. |
| Negative 2 | Codex asked which of 2024/2025 should receive the W-2 and requested the file; nothing was uploaded. |
| Negative 3 | Claude could begin an upload but could not send bytes because its sandbox could not resolve the upload host. No successful receipt was established. Verify the user-facing portal fallback before marking this case passed. |

Do not mark a case passed solely because OAuth or tool discovery succeeded.
Record the remaining results against the dedicated reviewer identity before
submission. Feature-flag-off credential redemption, expired auth, cancellation
and a fresh-account installation remain additional checks.

## Walkthrough to record

Use only the synthetic reviewer account. Hide credentials, consent codes,
access tokens and upload credentials throughout; never include them in a video.

1. Install the exact release package in the target assistant. Show its version.
2. Connect Current, complete OAuth, and show the connected state. Pause recording
   during credential entry. Separately confirm a reviewer can sign in without
   an interactive code.
3. Ask “Which returns can I send documents to?” Show only the synthetic client.
4. Ask “What is missing for my 2024 Form 1040?” Show the requested document.
5. Attach a synthetic matching file and confirm submission. Show the receipt and
   the same document in the portal, without exposing internal upload credentials.
6. Retry with the same key and show a single receipt. Show the ambiguous-year
   question and unavailable-client refusal from the negative cases.
7. Disconnect, demonstrate the observed access-token expiry behavior, reconnect,
   and successfully read requests again.
8. For a host that cannot upload, show the limitation and working portal fallback
   instead of claiming success. Do not present a Codex upload as a Claude upload.

Upload the recording to a reviewer-accessible location and set `walkthrough_url`
in `release.json`. This script is not a recording or evidence of a completed run.

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
