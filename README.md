# Current plugins

One document-collection skill and one OAuth-protected portal MCP connection,
packaged for OpenAI (ChatGPT/Codex) and Claude. Platform owns the server, access
controls, uploads and portal UI. This repository owns the installable packages.

| Provider | Installable folder | Distribution |
| --- | --- | --- |
| OpenAI | `codex/current` | Upload the generated ZIP to the Plugins portal |
| Claude | `claude` | Submit this GitHub folder to the developer portal |

Both folders are self-contained, committed packages. No build step is required
by the installing client. The shared skill remains authored in
`shared/skills/collect-documents/SKILL.md`; generated copies are checked in CI.

## Develop and package

Python 3.11+; no Python dependencies:

```sh
python3 scripts/release.py sync        # after changing shared skill or endpoint
python3 scripts/release.py check       # reject stale generated copies
python3 scripts/release.py build       # reproducible ZIPs + SHA256SUMS in dist/
claude plugin validate --strict claude
```

`release.json` owns the production endpoint. Do not put secrets or reviewer
credentials in this file or either package. Local/tunnel configurations belong
in a separate test copy, never in release packages.

## Release

```sh
python3 scripts/release.py probe       # read-only production OAuth/MCP check
python3 scripts/release.py submission  # also require publication metadata
```

See [RELEASE.md](RELEASE.md) for remaining submission decisions and the eight
review scenarios. Package validation is not provider approval or an authenticated
E2E test. Do not configure portal install buttons with this repository URL as a
substitute for verified provider listing links. No automatic publication occurs.
