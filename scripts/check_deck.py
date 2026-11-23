#!/usr/bin/env python3
"""Verify deck/manuscript consistency and source coverage, not browser behavior."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json,hashlib,re,sys

ROOT=Path(__file__).resolve().parents[1]
class Node:
    def __init__(self,tag='',attrs=None):self.tag=tag;self.attrs=dict(attrs or []);self.children=[]
    def text(self):return ''.join(c if isinstance(c,str) else c.text() for c in self.children)
    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child,Node):yield from child.walk()

class Parser(HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):super().__init__();self.root=Node();self.stack=[self.root]
    def handle_starttag(self,tag,attrs):
        n=Node(tag,attrs);self.stack[-1].children.append(n)
        if tag not in self.VOID:self.stack.append(n)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:self.stack=self.stack[:i];break
    def handle_data(self,data):self.stack[-1].children.append(data)

def at(obj,path):
    for part in path.split('.'):obj=obj[int(part)] if isinstance(obj,list) else obj[part]
    return obj

content=json.loads((ROOT/'slides/approved-content.json').read_text())
freeze=json.loads((ROOT/'reports/content-freeze.json').read_text())
outline=json.loads((ROOT/'slides/outline-data.json').read_text())
assert outline['status']=='user_approved','Outline must be approved'
assert hashlib.sha256((ROOT/'slides/approved-content.json').read_bytes()).hexdigest()==freeze['sha256']
deck=(ROOT/'slides/deck.html').read_text();p=Parser();p.feed(deck)
nodes=list(p.root.walk());slides=[n for n in nodes if 'slide' in n.attrs.get('class','').split()]
assert len(slides)==12
ids=[n.attrs['id'] for n in nodes if 'id' in n.attrs];assert len(ids)==len(set(ids)),'Duplicate IDs'
copied=[n for n in nodes if 'data-copy' in n.attrs]
for node in copied:assert node.text()==at(content,node.attrs['data-copy']),node.attrs['data-copy']
for i,slide in enumerate(slides):
    assert all(c=='slide' or c.startswith('layout-') for c in slide.attrs['class'].split()),'Slide/component classes must not collide'
    actual=[n for n in slide.walk() if 'data-claims' in n.attrs]
    assert len(actual)==1
    claims=re.findall(r'\[(S\d{2}-C\d{2})\]',actual[0].attrs['data-claims'])
    assert claims==content['slides'][i]['refs']
    assert any('source' in n.attrs.get('class','').split() for n in slide.walk())
    assert len([n for n in slide.walk() if n.tag=='h1'])==1
    for node in slide.walk():
        if node.tag=='a':
            href=node.attrs.get('href','')
            assert href.startswith('https://'),href
assert len([n for n in nodes if n.tag=='details' and 'self-check' in n.attrs.get('class','').split()])==3
assert len([n for n in nodes if n.tag=='option'])==12
assert not re.search(r'<script[^>]+src=',deck),'Deck must run offline'
assert not re.search(r'<link[^>]+stylesheet',deck),'Styles must be embedded'
assert (ROOT/'index.html').read_bytes()==(ROOT/'slides/deck.html').read_bytes()
assert len([n for n in nodes if n.tag=='svg'])==4
print(f'PASS: 12 slides; {len(copied)} fields match frozen manuscript verbatim')
print('PASS: unique IDs, per-page claims, source sections, 3 self-check questions, 12 navigation options')
print('PASS: standalone CSS/JS, root index matches deck, 4 labeled teaching pixel charts')
print('LIMIT: structure checks do not exercise browser clicks, keyboard focus, or responsive layout')
