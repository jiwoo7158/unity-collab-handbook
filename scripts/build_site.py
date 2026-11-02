#!/usr/bin/env python3
"""Build standalone GitHub Pages HTML from local Markdown; no runtime CDN."""
from pathlib import Path
from html import escape
import json, re, unicodedata
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'content'
OUT = ROOT/'docs'
OUT.mkdir(parents=True,exist_ok=True)
GROUPS = [
 ('시작하기',[
  ('00-intro','학습 안내'),('01-model','객체·DLL·참조'),('02-scope','변수·static·범위')]),
 ('1단계 · 코드 간 연결',[
  ('03-interface','Interface'),('04-delegate','Delegate'),('05-events','Event · Observer'),('06-dto','DTO · struct · record')]),
 ('2단계 · 의존성 설계',[
  ('07-di','Dependency Injection'),('08-patterns','Adapter · Facade')]),
 ('3단계 · 프로젝트 구조',[
  ('09-namespaces','Namespace · 접근 제한자'),('10-asmdef','Assembly Definition'),('11-unity','Unity 컴포넌트 · SO')]),
 ('4단계 · 협업과 통합',[
  ('12-tests','Unit · Integration Test'),('13-git-ci','Git · PR · CI'),('14-lab','종합 실습'),('15-troubleshooting','문제 해결'),('16-references','용어집 · 참고')])
]
CHAPTERS = [x for _,items in GROUPS for x in items]
chapter_lookup = {k:i for i,(k,_) in enumerate(CHAPTERS)}
formatter=HtmlFormatter(style='monokai',nowrap=True)

def slugify(s):
 s=unicodedata.normalize('NFKC',s.lower())
 s=re.sub(r'[^\w\-\s가-힣]','',s)
 return re.sub(r'[\s_]+','-',s).strip('-') or 'section'

def markdown_render(raw):
 md=MarkdownIt('commonmark',{'html':False,'typographer':True}).enable('table')
 toc=[];seen={}
 def heading_rule(renderer,tokens,idx,options,env):
  tok=tokens[idx]
  nxt=tokens[idx+1]
  name=tok.tag
  title=''.join(t.content for t in nxt.children or [] if t.type in ('text','code_inline')) or nxt.content
  slug=slugify(title);seen[slug]=seen.get(slug,0)+1
  if seen[slug]>1: slug=f'{slug}-{seen[slug]}'
  tok.attrSet('id',slug)
  if name in ('h2','h3'):toc.append((name,title,slug))
  return renderer.renderToken(tokens,idx,options,env)
 def fence_rule(renderer,tokens,idx,options,env):
  tok=tokens[idx]
  lang=(tok.info or '').strip().split(' ')[0].lower() or 'text'
  try:lex=get_lexer_by_name(lang,stripall=False)
  except:lex=TextLexer()
  highlighted=highlight(tok.content,lex,formatter)
  return '<div class="code-panel"><div class="code-bar"><span class="code-lang">'+escape(lang.upper())+'</span><button type="button" class="copy-code" aria-label="코드 복사">복사</button></div><pre class="highlight"><code>'+highlighted+'</code></pre></div>'
 md.add_render_rule('heading_open',heading_rule)
 md.add_render_rule('fence',fence_rule)
 return md.render(raw),toc

index_data=[]
for key,short in CHAPTERS:
 raw=(SRC/(key+'.md')).read_text(encoding='utf-8')
 title=raw.splitlines()[0].lstrip('# ').strip()
 body=re.sub(r'```[\s\S]*?```',' ',raw)
 body=re.sub(r'[#*`>\[\]|()]',' ',body)
 body=re.sub(r'\s+',' ',body)
 index_data.append({'title':title,'short':short,'url':key+'.html','text':body[:18000]})
search_json=json.dumps(index_data,ensure_ascii=False).replace('<','\\u003c').replace('</','<\\/')

def side_nav(active):
 parts=[]
 for group,chapters in GROUPS:
  parts.append(f'<div class="nav-group"><p class="nav-group-label">{escape(group)}</p>')
  for key,short in chapters:
   i=chapter_lookup[key];num=str(i).zfill(2)
   is_active=key==active
   parts.append(f'<a class="nav-link{" is-active" if is_active else ""}" href="{key}.html" {"aria-current=page" if is_active else ""}><span class="nav-num">{num}</span><span>{escape(short)}</span></a>')
  parts.append('</div>')
 return ''.join(parts)

def template(*,content,title,active=None,toc=(),home=False):
 nav=side_nav(active)
 toc_html=(''.join(f'<a class="toc-link {"toc-child" if lvl=="h3" else ""}" href="#{escape(slug)}">{escape(txt)}</a>' for lvl,txt,slug in toc) or '<p class="toc-empty">이 장의 목차 없음</p>')
 if active is not None:
  i=chapter_lookup[active]
  before=CHAPTERS[i-1] if i>0 else None
  after=CHAPTERS[i+1] if i<len(CHAPTERS)-1 else None
  prevnext='<nav class="chapter-pager" aria-label="이전과 다음 장">'
  if before:prevnext+=f'<a href="{before[0]}.html" class="pager-item"><small>← 이전 장</small><strong>{escape(before[1])}</strong></a>'
  else:prevnext+='<span></span>'
  if after:prevnext+=f'<a href="{after[0]}.html" class="pager-item pager-next"><small>다음 장 →</small><strong>{escape(after[1])}</strong></a>'
  prevnext+='</nav>'
 else:prevnext=''
 article=f'<article class="article markdown-body">{content}{prevnext}</article>'
 return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Unity C# 코드 협업: Interface, Delegate, Event, DTO, DI, asmdef, 테스트, PR을 코드로 배우는 실습 핸드북">
<meta name="theme-color" content="#f7f8fa"><title>{escape(title)} · Unity 코드 협업 핸드북</title>
<link rel="stylesheet" href="assets/site.css"><script defer src="assets/site.js"></script>
</head>
<body class="{'home-page' if home else 'chapter-page'}">
<div class="reading-progress" id="reading-progress"></div>
<header class="site-header">
 <button class="icon-button nav-toggle" id="nav-toggle" aria-label="목차 열기" title="목차 열기">☰</button>
 <a class="brand" href="index.html"><span class="brand-glyph">U<span class="brand-dot">.</span></span><span class="brand-text"><strong>Unity 코드 협업</strong><small>ENGINEERING HANDBOOK</small></span></a>
 <div class="header-actions"><button class="header-action" id="search-toggle" title="문서 검색 (/)" aria-label="문서 검색">⌕ <span>검색</span><kbd>/</kbd></button><button class="icon-button" id="theme-toggle" aria-label="테마 전환" title="테마 전환">◐</button><a class="header-link" href="00-intro.html">읽기 시작 <span>↗</span></a></div>
</header>
<div class="site-layout"><aside class="sidebar" id="sidebar"><div class="sidebar-inner"><a class="sidebar-home" href="index.html">⌂ <span>전체 로드맵</span></a><nav aria-label="챕터 탐색">{nav}</nav><div class="sidebar-footer"><span class="footer-indicator"></span> 소규모 Unity 팀을 위한 실무 학습서<br><small>HTML · 코드 예제 · 테스트</small></div></div></aside>
<main class="site-main" id="main"><div class="main-inner"><div class="breadcrumb"><a href="index.html">핸드북</a><span>/</span><span>{'개요' if home else escape(title)}</span></div>{article}<footer class="site-footer">© 학습용 가이드 · <a href="16-references.html">공식 참고 자료 및 검증 범위</a> · Unity와 GitHub의 상표는 각각의 권리자에게 귀속됩니다.</footer></div></main>
<aside class="toc" aria-label="현재 장 목차"><div class="toc-inner"><p class="toc-title">ON THIS PAGE</p>{toc_html}</div></aside></div>
<div class="mobile-overlay" id="mobile-overlay"></div>
<div class="search-dialog" id="search-dialog" role="dialog" aria-modal="true" aria-label="문서 검색" aria-hidden="true"><div class="search-shell"><div class="search-header"><span class="search-symbol">⌕</span><input id="search-input" autocomplete="off" placeholder="인터페이스, static, asmdef, 이벤트..." aria-label="검색어"/><button id="search-close" class="icon-button" aria-label="검색 닫기">✕</button></div><div id="search-results" class="search-results"><p class="search-hint">검색어를 입력하면 17개 장에서 찾아드립니다.</p></div><p class="search-footer">↑ ↓ 결과 이동 · Enter 열기 · Esc 닫기</p></div></div>
<script id="search-data" type="application/json">{search_json}</script>
</body></html>'''

for key,_ in CHAPTERS:
 raw=(SRC/(key+'.md')).read_text(encoding='utf8')
 content,toc=markdown_render(raw)
 title=raw.splitlines()[0].lstrip('# ').strip()
 (OUT/(key+'.html')).write_text(template(content=content,title=title,active=key,toc=toc),encoding='utf8')

steps=''.join(f'<a class="learning-card" href="{key}.html"><div class="learning-card-top"><span class="learning-num">{i:02d}</span><span class="learning-arrow">↗</span></div><h3>{escape(short)}</h3><p>{escape(index_data[i]["title"].split(". ",1)[-1])}</p></a>' for i,(key,short) in enumerate(CHAPTERS))
home_content='''
<section class="hero"><div class="hero-eyebrow"><span class="hero-mark"></span> UNITY · C# · TEAM ENGINEERING</div><h1>함께 만드는 코드는<br/><em>연결 방식부터</em> 설계한다.</h1><p class="hero-lead">인터페이스를 만들었는데 어디에 연결해야 할지 모르겠나요? 클래스·객체·변수 범위에서 시작해 계약, 이벤트, 의존성, 어셈블리, 테스트, PR까지. <strong>실제 Unity 파일 구조와 코드로 끝까지 따라가는 학습서.</strong></p><div class="hero-actions"><a class="primary-cta" href="00-intro.html">학습 시작하기 <span>→</span></a><a class="secondary-cta" href="14-lab.html">종합 실습 바로가기 ↗</a></div><div class="hero-stats"><div><strong>17<span>장</span></strong><small>개념부터 실습까지</small></div><div><strong>26<span>개</span></strong><small>Unity 실습 파일</small></div><div><strong>0<span>회</span></strong><small>외부 CDN 의존</small></div></div></section>
<section class="home-ribbon"><div><span class="ribbon-pill">하나의 연속 예제</span><h2>공격 → 체력 → UI</h2><p>팀원 A·B·C가 각자 만든 기능을 공통 계약과 통합 코드로 연결하고, 자동 테스트로 검증합니다.</p></div><div class="ribbon-steps"><span>AttackService</span><b>→</b><span>IDamageable</span><b>→</b><span>HealthModel</span><b>→</b><span>HealthOverlay</span></div></section>
<section class="home-roadmap"><div class="section-kicker">LEARNING PATH</div><h2>문서 목차</h2><p class="section-description">각 장은 개념 설명 · 정확한 문법 · 변수와 상태의 소유 범위 · 실제 파일 경로 · 실습 및 검증을 포함합니다.</p><div class="learning-grid">'''+steps+'''</div></section>
<section class="home-bottom"><h2>복사해서 직접 실행해 보세요.</h2><p><code>unity-example/Assets/_Game/</code> 폴더를 새 Unity 6 프로젝트에 복사하고, 메뉴에서 데모 씬을 생성하면 됩니다. GitHub Pages에서는 이 사이트의 <code>docs/</code>를 바로 게시할 수 있습니다.</p><a href="14-lab.html">실습 안내 보기 →</a></section>
'''
(OUT/'index.html').write_text(template(content=home_content,title='홈',home=True),encoding='utf8')
(OUT/'.nojekyll').write_text('',encoding='utf8')
print('Generated',len(CHAPTERS)+1,'HTML pages in',OUT)
