#!/usr/bin/env python3
"""Render frozen manuscript as a self-contained HTML teaching deck."""
from pathlib import Path
import json,hashlib,html,re,random,math

ROOT=Path(__file__).resolve().parents[1]
content_path=ROOT/'slides/approved-content.json'
CONTENT=json.loads(content_path.read_text())
freeze=json.loads((ROOT/'reports/content-freeze.json').read_text())
assert hashlib.sha256(content_path.read_bytes()).hexdigest()==freeze['sha256'],'Content changed: rerun content review before rendering'
S=CONTENT['slides']
CAT=json.loads((ROOT/'raw/source-catalog.json').read_text())['sources']
SOURCE={x['id']:x for x in CAT}
used=set()

def at(key):
    node=CONTENT
    for part in key.split('.'):
        node=node[int(part)] if isinstance(node,list) else node[part]
    return node

def copy(key,tag='p',cls=''):
    value=at(key);assert isinstance(value,str)
    used.add(key)
    return f'<{tag} class="{cls}" data-copy="{key}">{html.escape(value)}</{tag}>'

def label(i,n,tag='span',cls=''):
    return copy(f'slides.{i}.labels.{n}',tag,cls)

def flow(i,indices):
    return '<div class="flow">'+''.join('<div class="flow-node">'+label(i,n)+'</div>' for n in indices)+'</div>'

def bullets(i,field='points'):
    return '<ul class="points">'+''.join(copy(f'slides.{i}.{field}.{n}','li') for n in range(len(S[i][field])))+'</ul>'

def pixels(alpha,seed):
    rng=random.Random(seed);out=['<svg class="pixel-chart" viewBox="0 0 80 80" aria-hidden="true">']
    for y in range(8):
        for x in range(8):
            shape=(x in (2,5) and 1<=y<=6) or (y==3 and 2<=x<=5)
            signal=0.85 if shape else -0.85
            value=math.sqrt(alpha)*signal+math.sqrt(1-alpha)*rng.gauss(0,1)
            v=(max(-1,min(1,value))+1)/2
            low=(19,62,78);high=(231,243,233)
            rgb=tuple(round(a+(b-a)*v) for a,b in zip(low,high))
            out.append(f'<rect x="{x*10}" y="{y*10}" width="10" height="10" fill="rgb{rgb}"/>')
    out.append('</svg>');return ''.join(out)

def references(i):
    ids=list(dict.fromkeys(c[:3] for c in S[i]['refs']))
    rows=[]
    for sid in ids:
        rec=SOURCE[sid]
        text=(ROOT/rec['wiki_path']).read_text()
        selected=[line for line in text.splitlines() if any(line.startswith('| '+c+' ') for c in S[i]['refs'])]
        claims=''.join('<li>'+html.escape(line.strip('| ').replace(' | ',' · '))+'</li>' for line in selected)
        pdf=rec.get('pdf_url') or rec['url'].replace('/abs/','/pdf/')
        if sid=='S03':pdf='https://arxiv.org/pdf/2102.09672v1'
        if sid=='S02':pdf='https://arxiv.org/pdf/2010.02502v4'
        if sid=='S04':pdf='https://arxiv.org/pdf/2112.10752v2'
        if sid=='S05':pdf='https://arxiv.org/pdf/2208.11970v1'
        rows.append(f'<section><h3>{sid} · {html.escape(rec["title"])}</h3><p>{html.escape(rec["version"])} · <a href="{html.escape(pdf)}" target="_blank" rel="noopener noreferrer">原始論文</a></p><ul>{claims}</ul></section>')
    refs=' '.join('['+x+']' for x in S[i]['refs'])
    return f'<details class="source"><summary>來源依據 · {"、".join(ids)}</summary><div class="source-panel"><p class="source-intro">依 Wiki 來源主張表整理；點選原始論文可依章節與頁碼回查。</p>{"".join(rows)}</div></details><span class="claim-ids" data-claims="{refs}" aria-label="引用主張編號">{refs}</span>'

def body(i):
    p=f'slides.{i}';layout=S[i]['layout']
    if layout=='cover':
        return '<div class="cover-layout"><div>'+bullets(i)+'</div><div class="cover-words">'+label(i,0,'div')+label(i,1,'div')+'</div></div>'
    if layout=='concept':return '<div class="concept-flow">'+flow(i,[0,1,2])+'</div>'+bullets(i)
    if layout=='noise':
        out='<div class="noise-row">'
        for n,a in enumerate([1,.72,.25,.015]):out+='<figure>'+pixels(a,831)+label(i,n,'figcaption')+'</figure>'
        return out+'</div>'+bullets(i)
    if layout=='training':return '<div class="training-inputs">'+''.join(label(i,n,'div','input-token') for n in [0,1,2])+'</div>'+flow(i,[3,4,5])+'<div class="feedback-line">'+label(i,6)+label(i,7)+'</div>'+bullets(i)
    if layout=='network':return '<div class="network"><div class="network-input">'+label(i,0,'div')+label(i,1,'div')+'</div>'+label(i,2,'div','network-core')+label(i,3,'div','network-output')+'</div>'+bullets(i)
    if layout=='sampling':return flow(i,[0,1,2,3])+bullets(i)
    if layout=='compare':
        table='<div class="table-wrap"><table><thead><tr>'
        table+=''.join(copy(f'{p}.table.0.{n}','th') for n in range(3))+'</tr></thead><tbody>'
        for row in range(1,4):table+='<tr>'+''.join(copy(f'{p}.table.{row}.{n}','th' if n==0 else 'td') for n in range(3))+'</tr>'
        return table+'</tbody></table></div>'+bullets(i)
    if layout=='cost':return '<div class="cost-grid"><div class="cost-number">'+label(i,0,'strong')+label(i,1,'span')+'</div><div>'+bullets(i)+'</div></div><div class="cost-rule">'+label(i,2)+label(i,3)+'</div>'
    if layout=='methods':
        out='<div class="method-columns">'
        for c in [0,1]:
            out+='<section>'+label(i,c*2,'h2')+label(i,c*2+1,'p','method-sub')+'<ul class="points">'
            out+=''.join(copy(f'{p}.columns.{c}.{n}','li') for n in range(3))+'</ul></section>'
        return out+'</div>'
    if layout=='latent':return '<div class="latent-lane">'+label(i,0,'h2')+flow(i,[1,2,3,4])+'</div><div class="latent-lane second">'+label(i,5,'h2')+flow(i,[6,7,8,9])+'</div>'+bullets(i)
    if layout=='quiz':
        out='<div class="quiz-list">'
        for n in range(3):out+='<details class="self-check">'+copy(f'{p}.quiz.{n}.q','summary')+copy(f'{p}.quiz.{n}.a','p','quiz-answer')+'</details>'
        return out+'</div>'
    if layout=='references':
        out='<div class="reference-layout"><div>'+bullets(i)+'</div><ol class="bibliography">'
        for source in CAT:
            title=source['title'];sid=source['id'];url=source['url']
            out+=f'<li><span>{sid}</span><a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer">{html.escape(title)}</a></li>'
        return out+'</ol></div>'
    raise ValueError(layout)

CSS=r'''
:root{--ink:#143746;--teal:#167669;--coral:#be593f;--paper:#f6f8f7;--muted:#537078;--line:#d7e1df;--pale:#e4f0eb}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#e7eeec;color:var(--ink);font-family:"Noto Sans CJK TC","PingFang TC","Microsoft JhengHei",sans-serif;font-size:22px;font-size:clamp(18px,1.65vw,23px);line-height:1.65}a{color:var(--teal);text-underline-offset:4px}button,select,summary{font:inherit}button,select{border:1px solid #a9bdb6;background:#fff;color:var(--ink);border-radius:6px;padding:8px 15px;cursor:pointer;font-size:16px}button:hover{background:var(--pale)}button:disabled{opacity:.38;cursor:default}button:focus-visible,select:focus-visible,summary:focus-visible,a:focus-visible{outline:3px solid var(--coral);outline-offset:4px}.skip{position:fixed;top:-100px;left:15px;z-index:100;background:#fff;padding:12px}.skip:focus{top:12px}.masthead{max-width:1200px;margin:0 auto;padding:15px 4px 12px;display:flex;justify-content:space-between;font-size:14px;letter-spacing:.05em}.masthead span:last-child{color:var(--muted)}#deck{max-width:1200px;margin:0 auto}.slide{position:relative;background:var(--paper);padding:38px 48px 24px;margin-bottom:24px;min-height:690px;display:flex;flex-direction:column;border-top:5px solid var(--teal);box-shadow:0 8px 30px #163d4910;scroll-margin-top:15px}.slide[hidden]{display:none}.eyebrow{color:var(--teal);font-size:15px;letter-spacing:.14em;margin:0 0 12px}h1{font-size:44px;font-size:clamp(30px,3.4vw,46px);line-height:1.28;margin:0 0 16px;font-weight:700;letter-spacing:-.03em}h2{font-size:29px;line-height:1.35;margin:0 0 10px}.lead{font-size:25px;font-size:clamp(20px,1.95vw,27px);line-height:1.6;margin:0;max-width:1040px}.slide-body{margin:24px 0 15px;flex:1}.points{margin:16px 0;padding-left:1.15em}.points li{padding-left:.2em;margin:9px 0}.points li::marker{color:var(--teal)}.note{font-size:16px;line-height:1.7;color:var(--muted);margin:14px 0 18px;padding-left:14px;border-left:3px solid #9bb6ab}.slide-footer{border-top:1px solid var(--line);padding-top:12px;display:flex;justify-content:space-between;align-items:flex-start;gap:20px;font-size:14px}.page-count{white-space:nowrap;font-variant-numeric:tabular-nums;color:var(--muted)}.claim-ids{display:none}.source{position:relative;max-width:90%}.source summary{cursor:pointer;color:var(--teal);font-size:14px;list-style:none}.source summary::before{content:"＋ ";font-weight:bold}.source[open] summary::before{content:"－ "}.source-panel{position:absolute;bottom:32px;left:0;z-index:20;background:white;border:1px solid var(--line);border-radius:8px;padding:20px 24px;width:650px;max-width:calc(100vw - 80px);max-height:60vh;overflow:auto;box-shadow:0 10px 40px #1437462c;color:var(--ink);font-size:15px;line-height:1.7}.source-panel h3{font-size:17px;margin:14px 0 4px}.source-panel p{margin:4px 0}.source-panel ul{margin:8px 0;padding-left:20px}.source-panel li{margin:6px 0}.source-intro{color:var(--muted)}.cover{background:var(--ink);color:#fff;border-color:#78c4a6}.cover h1{font-size:76px;font-size:clamp(42px,6vw,80px);margin-top:20px}.cover .eyebrow,.cover .source summary{color:#9ed9be}.cover .lead{color:#b6d8ce;font-size:34px}.cover .note,.cover .page-count{color:#c5d8d2}.cover .slide-footer{border-color:#52727b}.cover-layout{display:flex;justify-content:space-between;align-items:center;gap:48px}.cover-layout>div:first-child{flex:1}.cover .points{max-width:650px;font-size:23px}.cover-words{min-width:230px;padding:25px 0 25px 32px;border-left:1px solid #71958d;font-size:37px;line-height:1.75;color:#a3d7bf}.flow{display:flex;align-items:stretch;gap:28px;margin:18px 0}.flow-node{flex:1;position:relative;padding:18px 15px;border:1.5px solid #8db4a8;border-radius:4px;text-align:center;display:flex;align-items:center;justify-content:center;background:#edf4f1;font-size:22px;line-height:1.5;min-width:0}.flow-node:not(:last-child)::after{content:"→";position:absolute;right:-25px;top:50%;transform:translateY(-50%);font-size:24px;color:var(--teal)}.concept-flow{margin:45px 0 38px}.concept-flow .flow-node{padding:35px 10px;border:none;border-bottom:3px solid var(--teal);background:transparent;font-size:26px}.noise-row{display:flex;gap:22px;margin:6px 0 24px}.noise-row figure{flex:1;min-width:0;margin:0;text-align:center}.pixel-chart{display:block;width:100%;max-width:200px;height:auto;margin:0 auto 10px;image-rendering:pixelated}.noise-row figcaption{font-size:19px;color:var(--muted)}.training-inputs{display:flex;justify-content:center;gap:28px;font-size:20px}.input-token{border-bottom:2px solid #9bb8b0;padding:5px 22px}.feedback-line{display:flex;justify-content:flex-end;gap:30px;font-size:18px;color:var(--coral);margin-top:-4px}.feedback-line span+span::before{content:"→ ";color:var(--coral)}.network{display:flex;align-items:center;gap:36px;margin:36px 0}.network-input,.network-output{flex:1;font-size:22px;text-align:center}.network-input>div{padding:12px;border-bottom:1px solid var(--line)}.network-core{flex:1.2;padding:40px 20px;background:var(--ink);color:white;text-align:center;font-size:39px;border-radius:3px;position:relative}.network-core::before,.network-core::after{position:absolute;top:50%;transform:translateY(-50%);color:var(--teal);font-size:28px}.network-core::before{content:"→";left:-29px}.network-core::after{content:"→";right:-29px}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:22px;line-height:1.6}th,td{text-align:left;padding:15px 18px;border-bottom:1px solid var(--line);vertical-align:top}thead th{background:var(--ink);color:white;font-weight:500}tbody th{width:22%;color:var(--teal);font-weight:500}tbody td{width:39%}.compare .points{font-size:18px}.cost-grid{display:flex;align-items:center;gap:45px}.cost-number{flex:0 0 34%;display:flex;flex-direction:column}.cost-number strong{font-size:112px;line-height:1.1;color:var(--teal);letter-spacing:-.07em}.cost-number span{font-size:17px;color:var(--muted);margin:10px 0}.cost-rule{margin-top:20px;padding-top:18px;border-top:1px solid var(--line);display:flex;justify-content:space-between;font-size:21px;color:var(--teal)}.method-columns{display:flex;gap:38px}.method-columns section{flex:1;min-width:0;border-top:4px solid var(--teal);padding-top:18px}.method-columns section+section{border-color:var(--coral)}.method-sub{color:var(--teal);font-size:19px;margin:0 0 12px}.method-columns section+section .method-sub{color:var(--coral)}.method-columns .points{font-size:21px;line-height:1.65}.latent-lane h2{font-size:18px;color:var(--teal);margin-bottom:3px}.latent-lane .flow{margin:8px 0 16px}.latent-lane .flow-node{font-size:18px;padding:14px 10px}.latent-lane.second h2{color:var(--coral)}.latent-lane.second .flow-node{background:#f8ede7;border-color:#d7a58f}.latent .points{font-size:19px}.quiz-list{margin-top:4px}.quiz{border-bottom:1px solid var(--line);padding:18px 0}.quiz summary{cursor:pointer;padding-left:8px;font-size:23px;font-weight:500}.quiz-answer{font-size:20px;background:var(--pale);padding:14px 20px;margin:12px 0 0}.reference-layout{display:flex;gap:35px;align-items:flex-start}.reference-layout>.points,.reference-layout>div{flex:1}.reference-layout .points{font-size:23px;margin-top:0}.bibliography{flex:1.25;list-style:none;margin:0;padding:0;font-size:17px;line-height:1.5}.bibliography li{padding:9px 0;border-bottom:1px solid var(--line);display:flex;gap:10px}.bibliography span{font-size:13px;color:var(--muted);padding-top:3px}.bibliography a{text-decoration-thickness:1px}.toolbar{position:sticky;bottom:0;z-index:40;background:#e7eecef5;background:rgba(231,238,236,.97);border-top:1px solid #bed0c8;padding:12px 20px;display:flex;align-items:center;justify-content:center;gap:12px;backdrop-filter:blur(8px)}.toolbar[hidden]{display:none}.toolbar select{max-width:370px;min-width:180px;padding-right:8px}.toolbar .hint{font-size:13px;color:var(--muted)}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.no-js{max-width:1200px;margin:10px auto;font-size:16px;padding:15px;background:white}body{padding:0 20px}.js .slide{margin-bottom:18px}.js[data-mode="all"] .slide{margin-bottom:25px}
@media(max-width:760px){body{padding:0 10px}.masthead{font-size:12px;padding:12px 4px}.masthead span:last-child{display:none}.slide{padding:25px 22px 18px;min-height:calc(100svh - 135px)}h1{font-size:31px}.lead{font-size:21px}.slide-body{margin:22px 0 10px}.points{font-size:19px}.note{font-size:14px;margin-bottom:14px}.cover h1{font-size:47px}.cover .lead{font-size:28px}.cover-layout{display:block}.cover .points{font-size:20px}.cover-words{display:flex;gap:18px;min-width:0;border-left:0;border-top:1px solid #52727b;padding:20px 0 0;font-size:25px}.flow{flex-wrap:wrap;gap:20px}.flow-node{flex-basis:calc(50% - 20px);font-size:18px;padding:14px 9px}.flow-node::after{display:none}.concept-flow{margin:20px 0}.concept-flow .flow{display:block}.concept-flow .flow-node{margin-bottom:13px;padding:15px;font-size:22px}.noise-row{flex-wrap:wrap;gap:18px}.noise-row figure{flex-basis:calc(50% - 18px)}.pixel-chart{max-width:155px}.noise-row figcaption{font-size:16px}.training-inputs{gap:10px;flex-wrap:wrap;font-size:17px}.input-token{padding:4px 6px}.feedback-line{font-size:16px;justify-content:center;gap:14px}.network{gap:16px;margin:20px 0;flex-direction:column}.network-input,.network-core,.network-output{width:100%;font-size:21px}.network-core{padding:25px;font-size:31px}.network-core::before,.network-core::after{display:none}.table-wrap{margin:0 -5px}table{font-size:17px;min-width:450px}th,td{padding:11px 10px}.compare .points{font-size:17px}.cost-grid{display:block}.cost-number strong{font-size:85px}.cost-number{margin:15px 0}.cost-rule{font-size:17px;gap:20px}.method-columns{display:block}.method-columns section{margin:20px 0 30px}.method-columns .points{font-size:19px}.latent-lane .flow-node{font-size:16px}.latent .points{font-size:18px}.quiz summary{font-size:20px}.quiz-answer{font-size:18px}.reference-layout{display:block}.bibliography{margin-top:22px;font-size:16px}.reference-layout .points{font-size:20px}.source-panel{max-width:calc(100vw - 60px);padding:16px;left:-4px;font-size:14px}.source summary{font-size:13px}.slide-footer{gap:10px;font-size:13px}.toolbar{gap:8px;padding:10px 4px;flex-wrap:wrap}.toolbar button,.toolbar select{font-size:14px;padding:7px 9px}.toolbar select{max-width:180px;min-width:120px}.toolbar .hint{display:none}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
@page{size:1280px 800px;margin:0}
@media print{html,body{width:1280px;margin:0!important;padding:0!important;background:white;font-size:22px}.masthead,.toolbar,.skip,.no-js{display:none!important}#deck{max-width:none;margin:0}.slide,.slide[hidden],.js .slide{display:flex!important;box-shadow:none;margin:0!important;width:1280px;height:800px;min-height:800px;padding:40px 50px 24px;break-after:page;page-break-after:always;overflow:hidden}.slide:last-child{break-after:auto;page-break-after:auto}h1{font-size:46px}.lead{font-size:27px}.cover h1{font-size:80px}.cover .lead{font-size:34px}.source-panel{display:none!important}.source summary{font-size:14px}.source summary::before{content:""}.quiz>p{display:block!important}.quiz{padding:12px 0}.quiz-answer{font-size:19px;padding:10px 16px;margin:8px 0}.quiz summary{font-size:22px}.noise-row figure{flex-basis:0}.source a{color:inherit}a{text-decoration:none}.flow-node{font-size:22px}.latent-lane .flow-node{font-size:18px}}
'''

JS=r'''
'use strict';
function nextSlideIndex(current,key,total){
  if(key==='Home')return 0;
  if(key==='End')return total-1;
  if(key==='ArrowRight'||key==='PageDown')return Math.min(total-1,current+1);
  if(key==='ArrowLeft'||key==='PageUp')return Math.max(0,current-1);
  return current;
}
(function(){
 const root=document.documentElement,slides=Array.from(document.querySelectorAll('.slide'));
 const bar=document.getElementById('toolbar'),select=document.getElementById('page-select');
 const prev=document.getElementById('previous'),next=document.getElementById('next');
 const all=document.getElementById('read-all'),status=document.getElementById('status');
 let current=0,allMode=false;
 function go(index){
  current=Math.max(0,Math.min(slides.length-1,Number.isFinite(index)?index:0));
  slides.forEach((slide,i)=>{slide.hidden=!allMode&&i!==current;slide.setAttribute('aria-label','第 '+(i+1)+' 頁，共 '+slides.length+' 頁');});
  select.value=String(current);select.disabled=allMode;
  prev.disabled=allMode||current===0;next.disabled=allMode||current===slides.length-1;
  status.textContent='第 '+(current+1)+' 頁，共 '+slides.length+' 頁：'+slides[current].querySelector('h1').textContent;
  if(!allMode){document.querySelectorAll('.source[open]').forEach(x=>x.removeAttribute('open'));try{history.replaceState(null,'','#slide-'+String(current+1).padStart(2,'0'));}catch(error){}window.scrollTo({top:0,behavior:'auto'});}
 }
 root.classList.add('js');bar.hidden=false;
 const match=location.hash.match(/^#slide-(\d+)$/);go(match?Number(match[1])-1:0);
 prev.addEventListener('click',()=>go(current-1));next.addEventListener('click',()=>go(current+1));
 select.addEventListener('change',()=>go(Number(select.value)));
 all.addEventListener('click',()=>{allMode=!allMode;root.dataset.mode=allMode?'all':'slides';all.textContent=allMode?'恢復翻頁':'全部閱讀';all.setAttribute('aria-pressed',String(allMode));go(current);});
 document.getElementById('print').addEventListener('click',()=>window.print());
 document.addEventListener('keydown',event=>{
  if(allMode||event.altKey||event.ctrlKey||event.metaKey||event.target.closest('input,textarea,select,[contenteditable="true"],details'))return;
  if(['ArrowLeft','ArrowRight','PageUp','PageDown','Home','End'].includes(event.key)){event.preventDefault();go(nextSlideIndex(current,event.key,slides.length));}
 });
})();
'''

CSS=re.sub(r'\.quiz(?![-a-zA-Z])','details.self-check',CSS)
for layout in ('cover','compare','latent'):
    CSS=re.sub(r'\.'+layout+r'(?![-a-zA-Z])','.layout-'+layout,CSS)
parts=[]
for i,s in enumerate(S):
    key=f'slides.{i}'
    article=f'<section class="slide layout-{s["layout"]}" id="slide-{i+1:02d}" data-slide="{i+1}" aria-labelledby="title-{i+1}">'
    article+=copy(key+'.eyebrow','p','eyebrow')+copy(key+'.title','h1').replace('<h1 ',f'<h1 id="title-{i+1}" ',1)+copy(key+'.lead','p','lead')
    article+='<div class="slide-body">'+body(i)+'</div>'+copy(key+'.note','p','note')
    article+='<footer class="slide-footer">'+references(i)+f'<span class="page-count">{i+1:02d} / 12</span></footer></section>'
    parts.append(article)

options=''.join(f'<option value="{i}">{i+1:02d} · {html.escape(s["title"])}</option>' for i,s in enumerate(S))
document=f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(CONTENT['title'])}</title><meta name="description" content="給初學者的十二頁擴散模型教學簡報，依五份文獻與 LLM Wiki 整理。"><meta name="content-sha256" content="{freeze['sha256']}"><style>{CSS}</style></head><body>
<a class="skip" href="#deck">跳到簡報內容</a><div class="masthead"><span>DIFFUSION · 擴散模型入門</span><span>12 頁教學簡報 · 來源可回查</span></div>
<noscript><p class="no-js">目前以全部閱讀方式顯示。啟用 JavaScript 後可使用翻頁、頁面選單與鍵盤導覽。</p></noscript>
<main id="deck">{''.join(parts)}</main>
<nav class="toolbar" id="toolbar" aria-label="簡報導覽" hidden><button type="button" id="previous">上一頁</button><label class="sr-only" for="page-select">選擇頁面</label><select id="page-select">{options}</select><button type="button" id="next">下一頁</button><button type="button" id="read-all" aria-pressed="false">全部閱讀</button><button type="button" id="print">列印</button><span class="hint">方向鍵翻頁 · Home / End</span></nav>
<p id="status" class="sr-only" role="status" aria-live="polite"></p>
<script>{JS}</script></body></html>'''

def all_copy_fields(slides):
    def walk(x,path):
        if isinstance(x,str):yield path
        elif isinstance(x,list):
            for n,v in enumerate(x):yield from walk(v,f'{path}.{n}')
        elif isinstance(x,dict):
            for k,v in x.items():
                if k not in ('refs','layout'):yield from walk(v,f'{path}.{k}')
    yield from walk(slides,'slides')

expected=set(all_copy_fields(S))
assert used==expected,{'missing':sorted(expected-used),'extra':sorted(used-expected)}
for path in (ROOT/'slides/deck.html',ROOT/'index.html'):
    path.write_text(document,encoding='utf-8')
(ROOT/'slides/deck-script.js').write_text(JS,encoding='utf-8')
print('Rendered 12 slides,',len(used),'verbatim content fields; standalone HTML bytes:',len(document.encode()))
