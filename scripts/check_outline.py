#!/usr/bin/env python3
"""Check planned slide/source coverage; does not validate slide semantics or layout."""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root/'slides/outline-data.json').read_text())
catalog = json.loads((root/'raw/source-catalog.json').read_text())['sources']
pages = data['pages']
errors = []
defined = set()
for source in catalog:
    if source['status'] == 'ingested':
        text = (root/source['wiki_path']).read_text()
        defined.update(re.findall(r'^\|\s*(S\d{2}-C\d{2})\s*\|',text,re.M))
if not 10 <= len(pages) <= 12:
    errors.append('Planned page count must be between 10 and 12')
if [p['page'] for p in pages] != list(range(1,len(pages)+1)):
    errors.append('Page numbers are not sequential')
coverage = {source['id']:[] for source in catalog if source['status']=='ingested'}
for page in pages:
    claims = set(page['claims'])
    if not claims or not claims <= defined:
        errors.append(f'Page {page["page"]}: missing or unknown claims')
    card_claims = set()
    for card in page['cards']:
        path = root/f'evidence/{card}.md'
        if not path.is_file():
            errors.append(f'Missing evidence card: {card}')
        else:
            card_claims.update(re.findall(r'\[(S\d{2}-C\d{2})\]',path.read_text()))
    if not claims <= card_claims:
        errors.append(f'Page {page["page"]}: claims not covered by the selected cards')
    if page['page'] != len(pages):
        for claim in claims:
            coverage.setdefault(claim[:3],[])
            if page['page'] not in coverage[claim[:3]]:
                coverage[claim[:3]].append(page['page'])
for sid, used in sorted(coverage.items()):
    print(f'{sid}: teaching pages {", ".join(map(str,sorted(used)))}')
    if not used:
        errors.append(f'{sid}: appears only on reference slide or not at all')
print(f'Planned pages: {len(pages)}')
print('Outline state:',data['status'])
if errors:
    for error in errors:print('FAIL:',error)
else:
    print('PASS: planned page count, claim IDs, evidence cards and teaching-source coverage')
pending=[]
if data['status']!='user_approved':pending.append('user confirmation')
if not (root/'slides/drafts.md').is_file():pending.append('final script')
pending+=['independent semantic review','real-browser interaction and responsive checks']
print('PENDING: '+', '.join(pending))
sys.exit(int(bool(errors)))
