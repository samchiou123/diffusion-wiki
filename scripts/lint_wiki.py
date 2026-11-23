#!/usr/bin/env python3
"""Check Wiki structure and source provenance; this does not verify meaning."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-five', action='store_true')
    parser.add_argument('--metadata-only', action='store_true', help='Public package: skip raw-byte presence and hash checks explicitly')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    errors = []
    for item in ('AGENTS.md', 'requirements.md', 'wiki/index.md', 'wiki/log.md'):
        if not (root / item).is_file():
            errors.append(f'Missing required file: {item}')
    catalog_path = root / 'raw/source-catalog.json'
    if not catalog_path.is_file():
        print('FAIL: Missing raw/source-catalog.json')
        return 1
    records = json.loads(catalog_path.read_text(encoding='utf-8'))['sources']
    ids = [s['id'] for s in records]
    if len(ids) != len(set(ids)):
        errors.append('Duplicate source ID')
    done = [s for s in records if s['status'] == 'ingested']
    identities = [s['identity'] for s in done]
    if len(identities) != len(set(identities)):
        errors.append('Multiple versions of one source counted separately')
    defined_claims = set()
    for source in done:
        path = root / source['wiki_path']
        if not path.is_file():
            errors.append(f'Missing source page: {source["wiki_path"]}')
            continue
        content = path.read_text(encoding='utf-8')
        claims = set(re.findall(r'^\|\s*(S\d{2}-C\d{2})\s*\|', content, re.M))
        if not claims:
            errors.append(f'No claim table: {source["wiki_path"]}')
        if any(not c.startswith(source['id'] + '-') for c in claims):
            errors.append(f'Claim/source ID mismatch: {source["id"]}')
        defined_claims.update(claims)
        raw = root / source['raw_path']
        if args.metadata_only:
            continue
        if not raw.is_file():
            errors.append(f'Missing raw file: {source["raw_path"]}')
        elif hashlib.sha256(raw.read_bytes()).hexdigest() != source['sha256']:
            errors.append(f'Raw SHA-256 mismatch: {source["raw_path"]}')
    if args.metadata_only:
        print('LIMIT: metadata-only public package check; raw PDF presence and SHA-256 NOT verified')
    checked_links = checked_claims = 0
    for path in root.rglob('*.md'):
        content = path.read_text(encoding='utf-8')
        content = re.sub(r'```.*?```', '', content, flags=re.S)
        for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', content):
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target) or target.startswith('#'):
                continue
            target = unquote(target.split('#', 1)[0])
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(f'Broken local link in {path.relative_to(root)}: {target}')
            checked_links += 1
        for claim in re.findall(r'\[(S\d{2}-C\d{2})\]', content):
            if claim not in defined_claims:
                errors.append(f'Unknown claim {claim}: {path.relative_to(root)}')
            checked_claims += 1
    index = root / 'wiki/index.md'
    index_text = index.read_text(encoding='utf-8') if index.is_file() else ''
    for folder in ('sources', 'concepts', 'comparisons', 'questions'):
        for path in (root / 'wiki' / folder).glob('*.md'):
            rel = path.relative_to(root / 'wiki').as_posix()
            if f']({rel})' not in index_text:
                errors.append(f'Wiki page missing from index: {rel}')
    print(f'Ingested distinct sources: {len(set(identities))}/5')
    print(f'Checked local links: {checked_links}; claim references: {checked_claims}')
    if args.require_five and len(set(identities)) < 5:
        errors.append('Readiness gate: fewer than five ingested distinct sources')
    if errors:
        for error in errors:
            print('FAIL:', error)
    else:
        print('PASS: structural checks; semantic fidelity not evaluated by this script')
    if len(set(identities)) < 5:
        print('PENDING: complete remaining ingests before making the teaching deck')
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
