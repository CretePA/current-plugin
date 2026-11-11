# Current plugins

Connect your assistant to Current. Find requested documents, send files to the
correct return, and check that Current received them.

This repo contains one shared skill and an MCP connection for each provider.
The server and portal code stay in the private platform repo.

| Provider | Plugin folder | Submission |
| --- | --- | --- |
| OpenAI | `chatgpt` | Upload the built ZIP to the Plugins portal |
| Claude | `claude` | Submit this folder through the developer portal |

## Build

Use Python 3.11 or later. No Python packages are required.

```sh
python3 scripts/release.py sync
python3 scripts/release.py check
python3 scripts/release.py build
claude plugin validate --strict claude
```

Edit the skill in `shared/skills/collect-documents/SKILL.md`. Run `sync` to update
both packages. Commit the generated files. Each plugin folder is ready to install;
the client does not need to build it.

`release.json` sets the production MCP URL. Keep credentials and local test URLs
out of this repo. ZIP files and checksums are written to `dist/`.

## Publish

```sh
python3 scripts/release.py probe       # Check public OAuth discovery
python3 scripts/release.py submission  # Check required listing fields too
```

See [RELEASE.md](RELEASE.md) for test results and submission steps. These commands
do not test authenticated uploads or publish a listing.

Claude requires this repo to be public before a plugin bundle can go live.
A standalone remote MCP connector does not require a public repo.
