/* 掌握度自评：所有页面复用（master 总览 / review 已学回顾 / calendar 学习日历）
   依赖：页面加载本文件后在卡片里写 <div class="assess" data-mid="4">…</div> 即可。
   API:
     GET  /api/mastery -> {sentences:[{id, mastery, reviewCount, lastReviewed, introduced}]}
     POST /api/mastery {id:int, action:'clear'|'fuzzy'|'unknown'} -> {ok, id, mastery}
   约定：句子 id 用数字字符串（如 '4'），带不带 's' 前缀都能识别。
   交互式控件统一 id：进度条 mbar-<id>  mbadge mb-<id>  状态 as-<id>。
*/
window.VocabMastery = (function () {
  const API_PORT = 3279;

  function num(sid) {
    return parseInt(String(sid == null ? '' : sid).replace(/[^0-9]/g, ''), 10);
  }

  async function post(sid, action) {
    const body = JSON.stringify({ id: num(sid), action });
    for (const base of ['http://127.0.0.1:' + API_PORT, '']) {
      try {
        const r = await fetch(base + '/api/mastery', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body
        });
        if (r && r.ok) { const j = await r.json(); return j; }
      } catch (e) {}
    }
    return null;
  }

  async function getMap() {
    for (const base of ['http://127.0.0.1:' + API_PORT, '']) {
      try {
        const r = await fetch(base + '/api/mastery');
        if (r && r.ok) {
          const j = await r.json();
          const m = {};
          (j.sentences || []).forEach(s => { m[s.id] = s.mastery; });
          return m;
        }
      } catch (e) {}
    }
    return null;
  }

  function mColor(v) { return v <= 2 ? '#dc2626' : (v <= 4 ? '#d97706' : '#16a34a'); }

  // 返回交互式自评控件 HTML（句子 id 为数字，如 '4'）
  function widgetHTML(sid) {
    sid = String(sid);
    return '<div class="assess" data-mid="' + sid + '">'
      + '<span class="lbl">自评掌握度：</span>'
      + '<div class="mbar" id="mbar-' + sid + '"><div class="mfill"></div></div>'
      + '<span class="mbadge" id="mb-' + sid + '">0/5</span>'
      + '<button class="c" onclick="VocabMastery.assess(\'' + sid + '\',\'clear\',this)">✅ 认识 +1</button>'
      + '<button class="f" onclick="VocabMastery.assess(\'' + sid + '\',\'fuzzy\',this)">🟡 模糊</button>'
      + '<button class="u" onclick="VocabMastery.assess(\'' + sid + '\',\'unknown\',this)">🔴 不认识 -1</button>'
      + '<span class="astat" id="as-' + sid + '"></span>'
      + '</div>';
  }

  function setBar(sid, v) {
    sid = String(sid);
    const bar = document.getElementById('mbar-' + sid);
    if (bar) {
      const f = bar.querySelector('.mfill');
      f.style.width = (v * 20) + '%';
      f.style.background = mColor(v);
    }
    const b = document.getElementById('mb-' + sid);
    if (b) b.textContent = v + '/5';
  }

  function setStat(btn, txt) {
    const w = btn.closest('.assess');
    const st = w && w.querySelector('.astat');
    if (st) st.textContent = txt;
  }

  async function assess(sid, action, btn) {
    sid = String(sid);
    const cur = parseInt(((document.getElementById('mb-' + sid) || {}).textContent || '0/5').replace('/5', ''), 10) || 0;
    let nv = cur;
    const r = await post(sid, action);
    if (r && typeof r.mastery === 'number') {
      nv = r.mastery;
      if (btn) setStat(btn, (action === 'clear' ? '已 +1' : action === 'unknown' ? '已 -1' : '已记录') + ' · 已回写 ✓');
    } else {
      nv = action === 'clear' ? Math.min(5, cur + 1) : action === 'unknown' ? Math.max(0, cur - 1) : cur;
      if (btn) setStat(btn, '已本地记录（启动本地服务后可回写）');
    }
    setBar(sid, nv);
    try { localStorage.setItem('vocab_mastery_' + num(sid), String(nv)); } catch (e) {}
    applyToStatic(num(sid), nv);
    if (btn) btn.blur();
    return nv;
  }

  // 同页面其它位置的该句掌握度也同步（master.html 旧 .mwrap 卡片、任何 [data-mastery] 元素）
  function applyToStatic(id, v) {
    const card = document.getElementById('s' + id);
    if (card) {
      card.setAttribute('data-mastery', v);
      const mw = card.querySelector('.mwrap');
      if (mw) {
        const lvl = v >= 5 ? 'lvl-green' : (v >= 3 ? 'lvl-yellow' : 'lvl-red');
        const seg = Array.from({ length: 5 }, (_, i) => '<i class="' + (i < v ? 'on' : '') + '"></i>').join('');
        mw.className = 'mwrap ' + lvl;
        const mb = mw.querySelector('.mbar');
        if (mb) { mb.className = 'mbar ' + lvl; mb.innerHTML = seg; }
        const mn = mw.querySelector('.mnum');
        if (mn) mn.textContent = v + '/5';
      }
    }
  }

  // 加载时把服务端最新掌握度应用到全部控件（让各页一致、互相同步）
  async function refreshAll() {
    const map = await getMap();
    if (!map) return false;
    for (const id in map) {
      const sid = String(id);
      setBar(sid, map[id]);
      applyToStatic(id, map[id]);
    }
    return true;
  }

  return { assess, setBar, refreshAll, widgetHTML, getMap, num };
})();
