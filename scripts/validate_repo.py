#!/usr/bin/env python3
"""Validate local static pages and Unity assembly reference graph (no Unity binary)."""
from pathlib import Path
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse,unquote

root=Path(__file__).resolve().parents[1]
site=root/'docs'
errors=[]
htmls=list(site.glob('*.html'))
for page in htmls:
 soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
 if not soup.select_one('h1'):errors.append(f'No h1: {page.name}')
 for tag in soup.select('a[href],link[href],script[src]'):
  ref=tag.get('href') or tag.get('src')
  u=urlparse(ref)
  if u.scheme or u.netloc or ref.startswith(('#','mailto:')):continue
  dest=(site/unquote(u.path))
  if not dest.exists():errors.append(f'{page.name}: broken link {ref}')
  elif u.fragment and dest.suffix=='.html':
   ids={t['id'] for t in BeautifulSoup(dest.read_text(encoding='utf-8'),'html.parser').select('[id]')}
   if unquote(u.fragment) not in ids:errors.append(f'{page.name}: missing anchor {ref}')
 if len(soup.select('nav[aria-label="챕터 탐색"] .nav-link'))!=17:
  errors.append(f'{page.name}: wrong nav links')

asm={}
for p in (root/'unity-example/Assets/_Game').rglob('*.asmdef'):
 try: d=json.loads(p.read_text(encoding='utf8'))
 except Exception as exc:errors.append(f'{p}: invalid JSON {exc}');continue
 if d['name'] in asm:errors.append(f'Duplicate assembly {d["name"]}')
 asm[d['name']]=(p,d.get('references',[]))
for name,(p,refs) in asm.items():
 for ref in refs:
  if ref not in asm:errors.append(f'{name}: missing assembly reference {ref}')

def visit(name,stack,done):
 if name in stack:errors.append('Cycle: '+' -> '.join(stack+[name]));return
 if name in done:return
 for ref in asm[name][1]:
  if ref in asm:visit(ref,stack+[name],done)
 done.add(name)
seen=set()
for name in asm:visit(name,[],seen)
expected={'00-intro','01-model','02-scope','03-interface','04-delegate','05-events','06-dto','07-di','08-patterns','09-namespaces','10-asmdef','11-unity','12-tests','13-git-ci','14-lab','15-troubleshooting','16-references'}
actual={p.stem for p in (root/'content').glob('*.md')}
if actual!=expected:errors.append('Chapters missing or extra: '+str(actual.symmetric_difference(expected)))
if len(htmls)!=18:errors.append('Expected 18 generated HTML pages, found '+str(len(htmls)))
if errors:
 print('\n'.join('ERROR '+e for e in errors))
 raise SystemExit(1)
print(f'PASS: {len(htmls)} HTML pages; {len(asm)} Unity assemblies; {len(actual)} chapters; local links and asmdef graph valid.')
