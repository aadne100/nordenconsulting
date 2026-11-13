#!/usr/bin/env python3
"""Validate local page links, media references and basic HTML before merging."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,p):
  super().__init__();self.path=p;self.tags=[];self.ids=[];self.h1=0;self.json=[];self.capture=False
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.tags.append((t,a));self.h1+=t=='h1'
  if a.get('id'):self.ids.append(a['id'])
  if t=='script' and a.get('type')=='application/ld+json':self.capture=True
 def handle_endtag(self,t):
  if t=='script':self.capture=False
 def handle_data(self,d):
  if self.capture:self.json.append(d)
pages={};errors=[];refs=[]
for p in ROOT.rglob('*.html'):
 if '.git' in p.parts:continue
 x=Page(p);x.feed(p.read_text());pages[p]=x
 if x.h1!=1:errors.append(f'{p.relative_to(ROOT)}: expected one h1')
 if len(x.ids)!=len(set(x.ids)):errors.append(f'{p.relative_to(ROOT)}: duplicate ID')
 for data in x.json:
  try:json.loads(data)
  except ValueError:errors.append(f'{p.name}: invalid JSON-LD')
 for t,a in x.tags:
  if t=='iframe':errors.append(f'{p.name}: iframe')
  if t=='img' and any(k not in a for k in ('alt','width','height')):errors.append(f'{p.name}: missing image alt/dimensions')
  for k in ('src','href','poster','data-preview'):
   if a.get(k):refs.append((p,a[k]))
  for c in a.get('srcset','').split(','):
   if c.strip():refs.append((p,c.strip().split()[0]))
for source,url in refs:
 u=urlsplit(url)
 if u.scheme=='data':errors.append('Embedded data URL');continue
 if u.scheme or u.netloc:continue
 target=(ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else source.parent/unquote(u.path)) if u.path else source
 target=target.resolve()
 if target.is_dir():target/='index.html'
 if not target.exists():errors.append(f'Missing: {target.relative_to(ROOT)}');continue
 if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'Missing anchor: {url}')
for p in ROOT.rglob('*'):
 if p.is_file() and '.git' not in p.parts and p.stat().st_size>=100_000_000:errors.append(f'Oversize: {p.name}')
errors=sorted(set(errors));print(f'{len(pages)} HTML pages, {len(refs)} references, {len(errors)} errors')
for e in errors:print(e)
sys.exit(bool(errors))
