#!/usr/bin/env python3
"""Build an installable Claude plugin with an explicit deployment endpoint."""
import argparse
import json
from pathlib import Path
import shutil
from urllib.parse import urlparse
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mcp-url', required=True)
parser.add_argument('--output', type=Path, required=True, help='New output directory')
args = parser.parse_args()
url = urlparse(args.mcp_url)
if (url.scheme != 'https' or not url.hostname or url.username or url.password
        or url.query or url.fragment or url.path != '/mcp/portal'):
    parser.error('--mcp-url must be an HTTPS /mcp/portal endpoint without credentials, query or fragment')
source = Path(__file__).resolve().parent
skill = source.parent / 'shared/skills/collect-documents'
if not (skill / 'SKILL.md').is_file():
    parser.error('shared collect-documents skill is missing')
args.output.mkdir(parents=True, exist_ok=False)
plugin = args.output / 'current'
shutil.copytree(source / '.claude-plugin', plugin / '.claude-plugin')
shutil.copytree(skill, plugin / 'skills/collect-documents')
shutil.copyfile(source / 'README.md', plugin / 'README.md')
config = json.loads((source / '.mcp.json.template').read_text())
config['mcpServers']['current']['url'] = args.mcp_url
(plugin / '.mcp.json').write_text(json.dumps(config, indent=2) + '\n')
archive = args.output / 'current-claude.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zipped:
    for file in sorted(plugin.rglob('*')):
        if file.is_file():
            zipped.write(file, file.relative_to(plugin))
print(plugin)
print(archive)
