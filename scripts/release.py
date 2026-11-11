#!/usr/bin/env python3
"""Sync, check and archive the two self-contained Current plugin packages."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {'openai': ROOT / 'codex', 'claude': ROOT / 'claude'}
MANIFESTS = {'openai': '.codex-plugin/plugin.json', 'claude': '.claude-plugin/plugin.json'}


def read_json(path):
    return json.loads(path.read_text())


def endpoint():
    value = read_json(ROOT / 'release.json')['mcp_url']
    url = urlparse(value)
    if (url.scheme != 'https' or not url.hostname or url.username or url.password
            or url.query or url.fragment or url.path != '/mcp/portal'
            or url.hostname in ('localhost', '127.0.0.1', '::1')
            or url.hostname.endswith('.trycloudflare.com')):
        raise ValueError('Release MCP URL must be a stable HTTPS /mcp/portal endpoint')
    return value


def generated_files():
    config = json.dumps({'mcpServers': {'current': {
        'type': 'http', 'url': endpoint(),
    }}}, indent=2).encode() + b'\n'
    skill = (ROOT / 'shared/skills/collect-documents/SKILL.md').read_bytes()
    for package in PACKAGES.values():
        yield package / 'LICENSE', (ROOT / 'LICENSE').read_bytes()
        yield package / '.mcp.json', config
        yield package / 'skills/collect-documents/SKILL.md', skill
    yield PACKAGES['openai'] / 'README.md', (PACKAGES['claude'] / 'README.md').read_bytes()


def check():
    for path, expected in generated_files():
        if not path.is_file() or path.read_bytes() != expected:
            raise ValueError(f'{path.relative_to(ROOT)} is stale; run scripts/release.py sync')
    versions = set()
    for provider, package in PACKAGES.items():
        manifest = read_json(package / MANIFESTS[provider])
        if manifest['name'] != 'current' or not manifest.get('description'):
            raise ValueError(f'{provider}: missing plugin identity')
        versions.add(manifest['version'])
        if manifest.get('mcpServers') != './.mcp.json':
            raise ValueError(f'{provider}: missing MCP reference')
        if len((package / 'README.md').read_text().split()) < 40:
            raise ValueError(f'{provider}: README too short')
        for path in package.rglob('*'):
            if path.is_symlink():
                raise ValueError(f'Package cannot contain symlinks: {path}')
            if path.is_file() and (path.suffix in ('.py', '.zip', '.template') or path.name.startswith('.env')):
                raise ValueError(f'Build-only or private file in package: {path}')
    if len(versions) != 1:
        raise ValueError('Provider package versions must match')
    print('Package consistency checks passed')


def probe():
    url = endpoint()
    discovery = url.removesuffix('/mcp/portal') + '/.well-known/oauth-protected-resource/mcp/portal'
    try:
        with urlopen(discovery, timeout=20) as response:
            metadata = json.load(response)
    except HTTPError as error:
        raise ValueError(
            f'Portal OAuth discovery returned HTTP {error.code} at {discovery}. '
            'Verify the portal MCP deployment and shared OAuth configuration before '
            'attempting plugin sign-in. WorkOS resource registration alone is insufficient.'
        ) from error
    if metadata.get('resource') != url or not metadata.get('authorization_servers'):
        raise ValueError('OAuth discovery must identify the exact portal resource and issuer')
    request = Request(url, data=b'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"current-release-check","version":"1.0"}}}',
                      headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'})
    try:
        with urlopen(request, timeout=20) as response:
            raise ValueError(f'Unauthenticated MCP request unexpectedly returned {response.status}')
    except HTTPError as error:
        if error.code != 401 or 'resource_metadata' not in error.headers.get('WWW-Authenticate', ''):
            raise ValueError('MCP must return 401 with OAuth resource metadata') from error
    print('Public OAuth discovery and unauthenticated MCP challenge passed; authenticated E2E still required')


def submission():
    check()
    missing = []
    for provider, package in PACKAGES.items():
        manifest = read_json(package / MANIFESTS[provider])
        if not manifest.get('license') and not (package / 'LICENSE').is_file():
            missing.append(f'{provider}: approved license')
    config = read_json(ROOT / 'release.json')
    for key in ('support_email', 'privacy_policy_url', 'walkthrough_url'):
        if not config.get(key):
            missing.append(key)
    if missing:
        raise ValueError('Submission incomplete: ' + ', '.join(missing))
    probe()
    print('Automated preflight passed. Complete the manual reviewer checklist in RELEASE.md.')


def build():
    check()
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    sums = []
    for provider, package in PACKAGES.items():
        version = read_json(package / MANIFESTS[provider])['version']
        archive = output / f'current-{provider}-{version}.zip'
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zipped:
            for path in sorted(package.rglob('*')):
                if path.is_file():
                    entry = zipfile.ZipInfo(path.relative_to(package).as_posix(), (2020, 1, 1, 0, 0, 0))
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    entry.external_attr = 0o100644 << 16
                    zipped.writestr(entry, path.read_bytes())
        sums.append(f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}')
        print(archive.relative_to(ROOT))
    (output / 'SHA256SUMS').write_text('\n'.join(sums) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['sync', 'check', 'build', 'probe', 'submission'])
    command = parser.parse_args().command
    if command == 'sync':
        for path, content in generated_files():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        check()
    else:
        globals()[command]()


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        sys.exit(str(error))
