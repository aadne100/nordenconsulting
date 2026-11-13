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
# Gallery entries are also image dependencies, not just metadata.
manifest=ROOT/'assets/media.json'
if manifest.exists():
 try:
  items=json.loads(manifest.read_text(encoding='utf-8'))
  if not isinstance(items,list):raise ValueError('expected a list')
  seen=set()
  for i,item in enumerate(items,1):
   if not isinstance(item,dict):
    errors.append(f'Media entry {i}: expected an object');continue
   for key in ('src','small'):
    value=item.get(key)
    if not isinstance(value,str) or not value.startswith('/assets/img/'):
     errors.append(f'Media entry {i}: invalid {key}');continue
    if not (ROOT/value.lstrip('/')).is_file():errors.append(f'Missing gallery media: {value}')
   if item.get('src') in seen:errors.append(f'Duplicate gallery media: {item.get("src")}')
   seen.add(item.get('src'))
   if not item.get('alt') or not item.get('group'):errors.append(f'Media entry {i}: missing alt or group')
  print(f'{len(items)} gallery entries checked')
 except (ValueError,UnicodeError) as exc:
  errors.append(f'Invalid assets/media.json: {exc}')
else:
 errors.append('Missing assets/media.json')
for p in ROOT.rglob('*'):
 if p.is_file() and '.git' not in p.parts and p.stat().st_size>=100_000_000:errors.append(f'Oversize: {p.name}')
errors=sorted(set(errors));print(f'{len(pages)} HTML pages, {len(refs)} references, {len(errors)} errors')
for e in errors:print(e)
sys.exit(bool(errors))
