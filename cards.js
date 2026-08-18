/* 共享卡片渲染：已学回顾 / 练习日历 复用
   依赖：在引用页先加载本文件，卡片容器可通过 renderSentenceCard(s) 生成 HTML 字符串再注入。
   s 结构：{id, en, zh, category, theme:'travel'|'daily', mastery:int,
            keyvocab:[{term,ipa,pos,zh}], enh:{fullIpa,variants,scenes,grammar,pron}} */
window.__en = {};
function esc2(x){
  return String(x==null?'':x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
function speak(text){ /* 已统一为服务器音频：用 speakId(id) -> playAudio(id) */ }
var __audioCache = {};
(function(){
  /* 隐藏容器：所有动态创建的 Audio 必须挂进 DOM 才能在远程浏览器（尤其手机）正常播放。
     仅 JS 变量持有引用不够——master.html(day 页) 的 audio 在卡片 DOM 里所以远程有声，
     review/calendar 走 cards.js 的 new Audio() 不在 DOM 中所以远程静音。 */
  var host = document.createElement('div');
  host.id = '__audioHost__';
  host.style.display = 'none';
  host.setAttribute('aria-hidden','true');
  (document.body || document.documentElement).appendChild(host);
  window.__audioHost = host;
})();
function playAudio(id, rate){
  const key = 's' + id;
  const realId = (String(id).indexOf('s') === 0) ? String(id) : key;
  let a = __audioCache[realId];
  if(!a){
    a = new Audio('audio/' + realId + '.mp3');
    __audioCache[realId] = a;
    window.__audioHost.appendChild(a);   /* 挂入 DOM：远程浏览器要求 audio 在 DOM 中才播放 */
  }
  a.playbackRate = rate || 1;
  try { a.currentTime = 0; } catch(e){}
  a.play().catch(e=>console.warn('audio play failed', e));
}
function speakId(id){ playAudio(id, 0.9); }
function masteryBadge(m){
  m = parseInt(m||0,10);
  const lvl = m>=5?'lvl-green':(m>=3?'lvl-yellow':'lvl-red');
  const seg = Array.from({length:5},(_,i)=>`<i class="${i<m?'on':''}"></i>`).join('');
  return `<div class="smbar ${lvl}">${seg}<span class="smnum">${m}/5</span></div>`;
}
function renderSentenceCard(s){
  const id = s.id;
  window.__en[id] = s.en;
  const enh = s.enh || {};
  const fi = enh.fullIpa || '';
  const v = (enh.variants||[]).map(x=>`<li><b>${esc2(x[0])}</b> <span class="dn">${esc2(x[1]||'')}</span></li>`).join('');
  const sc = (enh.scenes||[]).map(x=>`<li><span class="d-occ">${esc2(x[0])}</span> · <b>${esc2(x[1])}</b> → <span class="dn">${esc2(x[2]||'')}</span></li>`).join('');
  const kw = (s.keyvocab||[]).map(k=>`<span class="kv"><b>${esc2(k.term)}</b> <i>${esc2(k.ipa)}</i> <span class="pos">${esc2(k.pos||'')}</span> ${esc2(k.zh||'')}</span>`).join('');
  const badge = s.theme==='travel'?'旅游':'日常';
  const link = 'master.html#s'+id;
  const detId = 'det-'+id;
  const detRows = [
    fi?`<div class="d-row"><div class="d-k">整句音标</div><div class="d-v ipa">${esc2(fi)}</div></div>`:'',
    v?`<div class="d-row"><div class="d-k">口语变体</div><ul class="d-list">${v}</ul></div>`:'',
    sc?`<div class="d-row"><div class="d-k">场景用法</div><ul class="d-list">${sc}</ul></div>`:'',
    enh.grammar?`<div class="d-row"><div class="d-k">语法提示</div><div class="d-v">${esc2(enh.grammar)}</div></div>`:'',
    enh.pron?`<div class="d-row"><div class="d-k">发音提示</div><div class="d-v">${esc2(enh.pron)}</div></div>`:''
  ].join('');
  return `<div class="scard">
    <div class="stop">
      <span class="badge ${s.theme}">${badge}</span>
      <span class="cat">${esc2(s.category||'')}</span>
      <span class="play"><span class="ic" title="朗读原句" onclick="speakId(${id})">🔊</span></span>
    </div>
    <div class="sen">${esc2(s.en)}</div>
    <div class="sipa">${esc2(fi)}</div>
    <div class="szh">${esc2(s.zh)}</div>
    <div class="kvbox">${kw}</div>
    <button class="sdetBtn" onclick="toggleDet('${detId}')">🔤 发音详情 / 变体 / 场景 / 语法 ▾</button>
    <div class="sdet" id="${detId}">${detRows}</div>
    <div class="scfoot">${masteryBadge(s.mastery||0)}<a class="slink" href="${link}">在总览中查看 →</a></div>
  </div>`;
}
function toggleDet(id){
  const el = document.getElementById(id);
  if(el) el.classList.toggle('open');
}
