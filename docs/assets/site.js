(function(){
 'use strict';
 var root=document.documentElement;
 var themeBtn=document.getElementById('theme-toggle');
 function theme(next){root.dataset.theme=next;try{localStorage.setItem('uc-theme',next);}catch(e){}}
 try{if(localStorage.getItem('uc-theme')==='dark')root.dataset.theme='dark';}catch(e){}
 if(themeBtn)themeBtn.addEventListener('click',function(){theme(root.dataset.theme==='dark'?'light':'dark');});
 var navBtn=document.getElementById('nav-toggle');
 var overlay=document.getElementById('mobile-overlay');
 function closeNav(){document.body.classList.remove('nav-open');}
 if(navBtn)navBtn.addEventListener('click',function(){document.body.classList.toggle('nav-open');});
 if(overlay)overlay.addEventListener('click',closeNav);
 var prog=document.getElementById('reading-progress');
 function progress(){var h=document.documentElement;var total=h.scrollHeight-h.clientHeight;prog.style.width=(total>0?Math.min(100,100*h.scrollTop/total):0)+'%';}
 window.addEventListener('scroll',progress,{passive:true});progress();
 // Copy code from actual code text, not syntax-marked HTML.
 document.querySelectorAll('.copy-code').forEach(function(btn){btn.addEventListener('click',function(){
  var code=btn.closest('.code-panel').querySelector('code');var val=code.textContent;
  function done(){btn.textContent='복사됨 ✓';setTimeout(function(){btn.textContent='복사';},1600);}
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(val).then(done).catch(function(){fallback(val);done();});
  else{fallback(val);done();}
 });});
 function fallback(text){var el=document.createElement('textarea');el.value=text;el.style.position='fixed';el.style.opacity='0';document.body.appendChild(el);el.select();try{document.execCommand('copy');}catch(e){}el.remove();}
 var dialog=document.getElementById('search-dialog');var input=document.getElementById('search-input');var results=document.getElementById('search-results');
 var data=[];try{data=JSON.parse(document.getElementById('search-data').textContent);}catch(e){}
 function openSearch(){dialog.classList.add('open');dialog.setAttribute('aria-hidden','false');input.focus();renderResults();}
 function closeSearch(){dialog.classList.remove('open');dialog.setAttribute('aria-hidden','true');}
 document.getElementById('search-toggle').addEventListener('click',openSearch);
 document.getElementById('search-close').addEventListener('click',closeSearch);
 dialog.addEventListener('mousedown',function(e){if(e.target===dialog)closeSearch();});
 function norm(s){return(s||'').toLocaleLowerCase();}
 function escape(s){return(s||'').replace(/[&<>"']/g,function(x){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x];});}
 function renderResults(){var q=norm(input.value.trim());if(!q){results.innerHTML='<p class="search-hint">검색어를 입력하면 17개 장에서 찾아드립니다.</p>';return;}
  var matches=data.map(function(r){var text=norm(r.title+' '+r.short+' '+r.text);var pos=text.indexOf(q);var score=norm(r.title).includes(q)?3:norm(r.short).includes(q)?2:pos>=0?1:0;return {r:r,score:score};}).filter(function(x){return x.score>0;}).sort(function(a,b){return b.score-a.score;}).slice(0,12);
  if(!matches.length){results.innerHTML='<p class="search-empty">검색 결과가 없습니다. 다른 키워드를 입력해 보세요.</p>';return;}
  results.innerHTML=matches.map(function(x){var idx=norm(x.r.text).indexOf(q);var excerpt=idx>=0?x.r.text.slice(Math.max(0,idx-47),idx+100):x.r.text.slice(0,120);return '<a class="search-result" href="'+encodeURI(x.r.url)+'"><strong>'+escape(x.r.title)+'</strong><small>'+escape(excerpt)+'…</small></a>';}).join('');
 }
 input.addEventListener('input',renderResults);
 document.addEventListener('keydown',function(e){if((e.key==='/'&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&document.activeElement!==input&&document.activeElement.tagName!=='TEXTAREA')||(e.key==='k'&&(e.metaKey||e.ctrlKey))){e.preventDefault();openSearch();}else if(e.key==='Escape'){closeSearch();closeNav();}else if(e.key==='Enter'&&document.activeElement===input){var a=results.querySelector('a');if(a)window.location.href=a.href;}});
})();
