# Release checklist

The packages use `https://app.current.co/mcp/portal`.

## Before submission

- Set a monitored `support_email` and a reviewer-accessible `walkthrough_url` in
  `release.json`. The privacy policy URL is already set.
- Confirm publisher access. Have the responsible owner review the legal and
  data-handling statements.
- Test the reviewer login and the scenarios below. Keep credentials out of this
  repo and recordings.

OpenAI confirmed an email-code review flow for this submission. The reviewer
identity now has Member access to the synthetic client and the agent feature flag.
The reviewer must still complete sign-in and OAuth. Enter instructions under
**Review information → Review details → Magic link or email code** in the OpenAI
portal. No global authentication change is required.

Claude needs its own reviewer access instructions. Do not reuse OpenAI's reviewer
identity for Claude.

## Build and submit

1. Update both manifest versions when making a release.
2. Run `python3 scripts/release.py sync`, `check`, and `build`.
3. Run `claude plugin validate --strict claude` and the OpenAI plugin validator.
4. Run `python3 scripts/release.py submission`.
5. OpenAI: upload `dist/current-openai-<version>.zip` at
   <https://platform.openai.com/plugins>. Complete OAuth, domain verification,
   listing fields, and review materials.
6. Claude: submit the production MCP as a connector, then submit
   `CretePA/current-plugin` with plugin path `claude` at
   <https://claude.ai/directory/manage>. Use the Current publisher account.
7. Resolve validation findings and submit for review.
8. After approval, publish and test installation from the listing. Use the
   verified listing URLs in the portal.

Claude allows private source validation through an authorized GitHub connection.
The repo must be public before a plugin bundle goes live. A standalone MCP
connector requires only a server URL. The hosted server code can stay private.

## Test results

These results use synthetic production data. They do not prove upload support in
every assistant.

| Check | Result |
| --- | --- |
| Public OAuth discovery and 401 challenge | Passed November 5, 2026. |
| Codex discovery and request reads | Passed November 5. Only the synthetic client's general, 2024, and 2025 destinations were returned. |
| Codex upload | Passed. Receipt and accountant UI agreed on the 2024 return. Stored-byte checksum comparison remains untested. |
| Codex retry | Same key returned the same file ID and one receipt. |
| Reconnect | Both hosts reconnected. Codex read requests; Claude showed tools. Cached Codex access still worked after revocation. Rejection after token expiry remains untested. |
| Ambiguous year | Codex asked which year to use and did not upload. |
| Unavailable client | Codex stopped when the client was absent from authorized destinations. A direct unauthorized-ID request remains untested. |
| Claude personal installation and OAuth | Passed November 11 with plugin 0.1.0. |
| Claude personal reads | Destination, request, and receipt tools passed November 11. |
| Claude personal upload | Not completed. Claude reported networking disabled and stopped before issuing upload credentials. No test-file receipt was created. |
| Claude Team/Cowork and ChatGPT upload | Not verified. |

Do not describe Claude personal uploads as working. Confirm the portal fallback
and test a Claude runtime with file access and outbound HTTP.

## Reviewer scenarios

Record the host, package version, date, result, and receipt for each test.

1. List authorized destinations. Confirm that only the test client appears.
2. Read requests for the selected return. Do not treat “matched” as reviewed.
3. Upload a synthetic file after confirmation. Match the response ID to its receipt.
4. Retry with the same idempotency key. Confirm there is no duplicate file.
5. Disconnect, test access after token expiry, reconnect, and read requests again.
6. Request an unauthorized client. Confirm that no data or upload access is granted.
7. Leave the year unclear. Confirm that the assistant asks before uploading.
8. Use a host without upload capability. Confirm a clear explanation and a working
   portal fallback, with no claim of delivery.

Also check a fresh account, expired authentication, cancelled consent, and upload
credential redemption with the feature flag off.

## Record the walkthrough

Show installation, OAuth, document requests, upload, receipt, retry, and reconnect.
Pause during sign-in. Hide codes, tokens, and upload credentials. Show the portal
fallback when a host cannot upload. Do not use a Codex upload as evidence of a
Claude upload.

Upload the recording and set `walkthrough_url`. A script is not test evidence.

## Release notes: 0.1.0

First release. One skill and one portal MCP connection. Supports document requests,
upload authorization, and receipts. File transfer requires an assistant with file
access and outbound HTTP. Other hosts use portal upload.

## References

- [Claude publication](https://claude.com/docs/directory/publish)
- [OpenAI submission](https://developers.openai.com/plugins/deploy/submission)
