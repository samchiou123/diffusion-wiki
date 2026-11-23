
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
