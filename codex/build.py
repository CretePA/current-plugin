#!/usr/bin/env python3
"""Build a Current Codex plugin with an explicit portal MCP endpoint."""
import argparse
import json
from pathlib import Path
import shutil
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mcp-url', required=True)
parser.add_argument('--output', type=Path, required=True, help='New output directory; must be named current')
args = parser.parse_args()
url = urlparse(args.mcp_url)
if (url.scheme != 'https' or not url.hostname or url.username or url.password
        or url.query or url.fragment or url.path != '/mcp/portal'):
    parser.error('--mcp-url must be an HTTPS /mcp/portal endpoint without credentials, query or fragment')
if args.output.name != 'current' or args.output.exists():
    parser.error('--output must be a new directory named current')
source = Path(__file__).resolve().parent
shutil.copytree(source / 'current', args.output)
shutil.copytree(source.parent / 'shared/skills', args.output / 'skills')
(args.output / '.mcp.json').write_text(json.dumps({
    'mcpServers': {'current': {'type': 'http', 'url': args.mcp_url}},
}, indent=2) + '\n')
manifest_path = args.output / '.codex-plugin/plugin.json'
manifest = json.loads(manifest_path.read_text())
manifest['mcpServers'] = './.mcp.json'
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
print(args.output.resolve())
