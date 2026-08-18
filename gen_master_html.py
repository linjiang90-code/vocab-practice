import json, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("master.json", "r", encoding="utf-8") as f:
    data = json.load(f)

S = data["sentences"]
meta = data["meta"]
cats = sorted(set(s["category"] for s in S))

def esc(x):
    return (str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def render_detail(s):
    enh = s.get("learn", {}).get("enh", {})
    parts = []
    fi = enh.get("fullIpa", "")
    if fi:
        parts.append(f'<div class="d-row"><div class="d-k">整句音标</div><div class="d-v ipa">{esc(fi)}</div></div>')
    pr = enh.get("pron", "")
    if pr:
        parts.append(f'<div class="d-row"><div class="d-k">发音提示</div><div class="d-v">{esc(pr)}</div></div>')
    vs = enh.get("variants", []) or []
    if vs:
        items = "".join(
            f'<li><b>{esc(v[0])}</b> <span class="dn">{esc(v[1]) if len(v) > 1 else ""}</span></li>'
            for v in vs
        )
        parts.append(f'<div class="d-row"><div class="d-k">口语变体</div><ul class="d-list">{items}</ul></div>')
    sc = enh.get("scenes", []) or []
    if sc:
        items = "".join(
            f'<li><span class="d-occ">{esc(x[0])}</span> · <b>{esc(x[1])}</b> → <span class="dn">{esc(x[2]) if len(x) > 2 else ""}</span></li>'
            for x in sc
        )
        parts.append(f'<div class="d-row"><div class="d-k">场景用法</div><ul class="d-list">{items}</ul></div>')
    gm = enh.get("grammar", "")
    if gm:
        parts.append(f'<div class="d-row"><div class="d-k">语法提示</div><div class="d-v">{esc(gm)}</div></div>')
    if not parts:
        return ('<div class="d-empty">完整音变 / 变体 / 场景 / 语法标注将在该句被每日推送学习时自动生成 ✨'
                '<br>目前可先用 🔁 朗读 + 生词音标学习。</div>', False)
    return "\n".join(parts), True

cards = ""
for s in S:
    readwrap = f'''
      <div class="readwrap">
        <span class="rlbl">🔁 朗读</span>
        <select class="repsSel" data-id="{s['id']}">
          <option value="2">2 遍</option>
          <option value="3" selected>3 遍</option>
          <option value="5">5 遍</option>
          <option value="8">8 遍</option>
        </select>
        <button class="readBtn" data-id="{s['id']}">▶ 开始</button>
        <span class="spdlbl">语速</span>
        <select class="spdSel" data-id="{s['id']}">
          <option value="1">1.0x</option>
          <option value="0.75">0.75x</option>
          <option value="0.5">0.5x</option>
          <option value="0.4">0.4x</option>
        </select>
      </div>'''
    kv = "".join(
        f'<span class="kv"><b>{esc(k["term"])}</b> <i>{esc(k["ipa"])}</i> '
        f'<span class="pos">{esc(k.get("pos",""))}</span> {esc(k.get("zh",""))}</span>'
        for k in s["keyvocab"]
    )
    badge = "旅游" if s["theme"] == "travel" else "日常"
    lng = "长句" if s["length"] == "long" else "短句"
    learned = bool(s.get("learn", {}).get("introduced"))
    mastery = int(s.get("learn", {}).get("mastery", 0) or 0)
    lvl = "lvl-green" if mastery >= 5 else ("lvl-yellow" if mastery >= 3 else "lvl-red")
    seg = "".join(f'<i class="{"on" if i < mastery else ""}"></i>' for i in range(5))
    mastery_html = (f'<div class="mwrap {lvl}"><span class="mlbl">掌握度</span>'
                    f'<span class="mbar {lvl}">{seg}</span><span class="mnum">{mastery}/5</span></div>')
    detail_html, has = render_detail(s)
    toggle_label = "🔤 发音详情 ▾" if has else "🔤 完整增强（待生成）▾"
    toggle_cls = "toggle ready" if has else "toggle wait"
    cards += f'''
    <div class="card" id="s{s['id']}" data-theme="{s['theme']}" data-cat="{esc(s['category'])}" data-learned="{"yes" if learned else "no"}" data-mastery="{mastery}">
      <div class="top">
        <span class="badge {s['theme']}">{badge}</span>
        <span class="lng lng-{s['length']}">{lng}</span>
        <span class="cat">{esc(s['category'])}</span>
        <span class="sid">#{s['id']}</span>
      </div>
      <div class="en">{esc(s['en'])}</div>
      <div class="zh">{esc(s['zh'])}</div>
      <div class="kvbox">{kv}</div>
      {readwrap}
      {mastery_html}
      <button class="{toggle_cls}" onclick="this.parentElement.querySelector('.detail').classList.toggle('open')">{toggle_label}</button>
      <div class="detail">{detail_html}</div>
    </div>'''

catbtns = "".join(f'<button class="fbtn" data-cat="{esc(c)}">{esc(c)}</button>' for c in cats)

# 顶部总进度统计
total = len(S)
learned = sum(1 for s in S if s.get("learn", {}).get("introduced"))
sum_all = sum(int(s.get("learn", {}).get("mastery", 0) or 0) for s in S)
sum_learned = sum(int(s.get("learn", {}).get("mastery", 0) or 0) for s in S if s.get("learn", {}).get("introduced"))
avg_learned = (sum_learned / learned) if learned else 0
avg_str = f"{avg_learned:.1f}"
pct_all = round(sum_all / total / 5 * 100) if total else 0
gcolor = "#16a34a" if (sum_all / total) >= 5 else ("#d97706" if (sum_all / total) >= 3 else "#dc2626")
stats_html = f'''<div class="stats">
      <div class="stat"><span class="num" id="stLearned">{learned}</span><span class="lbl">/ <span id="stTotal">{total}</span> 已学句数</span></div>
      <div class="stat"><span class="num" id="stAvg">{avg_str}</span><span class="lbl">/ 5 平均掌握度<span class="hint">（已学句口径）</span></span></div>
      <div class="gbarwrap"><div class="gbar"><i id="stBar" style="width:{pct_all}%;background:{gcolor}"></i></div><span class="glbl" id="stPct">总掌握度 {pct_all}%</span></div>
    </div>'''

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>旅游+日常英语 {total} 范式 · 总览</title>
<style>
  :root {{
    --bg:#f5f7fa; --card:#ffffff; --ink:#1f2933; --sub:#6b7280;
    --travel:#2563eb; --daily:#0d9488; --line:#e5e7eb; --accent:#f59e0b;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,"PingFang SC","Microsoft YaHei",Segoe UI,sans-serif;
    background:var(--bg); color:var(--ink); }}
  header {{ background:linear-gradient(120deg,#2563eb,#0d9488); color:#fff; padding:20px 24px; display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap; }}
  .htitle h1 {{ margin:0 0 6px; font-size:22px; }}
  .htitle p {{ margin:0; opacity:.92; font-size:13px; }}
  details.legend-box {{ background:#fff7ed; border:1px solid #fed7aa; border-radius:8px; color:#9a3412;
    font-size:12px; margin:10px 16px 0; }}
  details.legend-box > summary {{ cursor:pointer; padding:8px 16px; font-weight:600; list-style:none;
    user-select:none; }}
  details.legend-box > summary::-webkit-details-marker {{ display:none; }}
  details.legend-box > summary::before {{ content:"▸ "; }}
  details.legend-box[open] > summary::before {{ content:"▾ "; }}
  .legend-body {{ padding:0 16px 10px; line-height:1.6; }}
  .legend-body b {{ color:#b45309; }}
  .bar {{ position:sticky; top:0; background:#fff; border-bottom:1px solid var(--line);
    padding:10px 16px; display:flex; flex-wrap:wrap; gap:6px; align-items:center; z-index:5; }}
  .bar .grp {{ display:flex; flex-wrap:wrap; gap:6px; }}
  button.fbtn {{ border:1px solid var(--line); background:#fff; color:var(--ink);
    border-radius:999px; padding:5px 12px; font-size:12px; cursor:pointer; }}
  button.fbtn:hover {{ border-color:var(--travel); }}
  button.fbtn.on {{ background:var(--travel); color:#fff; border-color:var(--travel); }}
  button.tbtn {{ border:1px solid var(--line); background:#fff; border-radius:8px; padding:5px 12px;
    font-size:12px; cursor:pointer; }}
  button.tbtn.on {{ background:var(--daily); color:#fff; border-color:var(--daily); }}
  .count {{ margin-left:auto; font-size:12px; color:var(--sub); }}
  button#filterToggle {{ border:1px dashed #cbd5e1; background:#f1f5f9; border-radius:8px; padding:5px 12px;
    font-size:12px; cursor:pointer; }}
  button#filterToggle:hover {{ border-color:var(--travel); }}
  .filtersBody {{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; }}
  .filtersBody.collapsed {{ display:none; }}
  .speedWrap {{ font-size:12px; color:var(--sub); display:flex; align-items:center; gap:5px; margin-left:6px; }}
  .speedWrap select {{ border:1px solid var(--line); background:#fff; border-radius:8px; padding:5px 8px;
    font-size:12px; color:var(--ink); cursor:pointer; }}
  .mwrap {{ display:flex; align-items:center; gap:6px; margin:8px 0 2px; font-size:12px; }}
  .mlbl {{ color:var(--sub); }}
  .mbar {{ display:flex; gap:3px; }}
  .mbar i {{ width:22px; height:7px; border-radius:3px; background:#e2e8f0; display:inline-block; }}
  .mbar.lvl-red i.on {{ background:linear-gradient(90deg,#ef4444,#dc2626); }}
  .mbar.lvl-yellow i.on {{ background:linear-gradient(90deg,#f59e0b,#d97706); }}
  .mbar.lvl-green i.on {{ background:linear-gradient(90deg,#22c55e,#16a34a); }}
  .mnum {{ font-weight:600; margin-left:2px; }}
  .mwrap.lvl-red .mnum {{ color:#dc2626; }}
  .mwrap.lvl-yellow .mnum {{ color:#d97706; }}
  .mwrap.lvl-green .mnum {{ color:#16a34a; }}
  .card[data-learned="no"] .mnum {{ color:#cbd5e1; }}
  .stats {{ display:flex; align-items:center; flex-wrap:wrap; gap:18px; background:#fff; border-bottom:1px solid var(--line);
    padding:12px 24px; }}
  .stat {{ display:flex; align-items:baseline; gap:4px; }}
  .stat .num {{ font-size:22px; font-weight:800; color:var(--travel); }}
  .stat .lbl {{ font-size:12px; color:var(--sub); }}
  .gbarwrap {{ display:flex; align-items:center; gap:10px; margin-left:auto; }}
  .gbar {{ width:220px; height:10px; background:#e2e8f0; border-radius:999px; overflow:hidden; }}
  .gbar i {{ display:block; height:100%; border-radius:999px; transition:width .3s; }}
  .glbl {{ font-size:12px; color:var(--sub); }}
  .hint {{ font-size:10px; color:#94a3b8; margin-left:2px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:14px;
    padding:16px; max-width:1200px; margin:0 auto; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:14px 16px;
    box-shadow:0 1px 3px rgba(0,0,0,.04); }}
  .top {{ display:flex; align-items:center; gap:8px; margin-bottom:8px; }}
  .badge {{ font-size:11px; padding:2px 8px; border-radius:6px; color:#fff; }}
  .badge.travel {{ background:var(--travel); }}
  .badge.daily {{ background:var(--daily); }}
  .lng {{ font-size:11px; padding:2px 8px; border-radius:6px; background:#f1f5f9; color:var(--sub); }}
  .lng.long {{ background:#fef3c7; color:#b45309; }}
  .cat {{ font-size:12px; color:var(--sub); }}
  .sid {{ margin-left:auto; font-size:11px; color:#cbd5e1; }}
  .en {{ font-size:17px; font-weight:600; line-height:1.4; margin:4px 0; }}
  .zh {{ font-size:14px; color:var(--sub); margin-bottom:8px; }}
  .kvbox {{ display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }}
  .kv {{ font-size:12px; background:#f8fafc; border:1px solid var(--line); border-radius:6px;
    padding:3px 7px; }}
  .kv b {{ color:var(--ink); }}
  .kv i {{ color:#be123c; font-style:normal; font-family:"Cambria Math",Georgia,serif; }}
  .kv .pos {{ color:#0891b2; }}
  audio {{ width:100%; height:34px; }}
  .readwrap {{ display:flex; flex-wrap:wrap; align-items:center; gap:6px; margin:6px 0 2px; font-size:12px; color:var(--sub); }}
  .readwrap select {{ border:1px solid var(--line); background:#fff; border-radius:8px; padding:4px 7px; font-size:12px; color:var(--ink); cursor:pointer; }}
  .readwrap .rlbl {{ font-weight:600; color:#475569; }}
  .readwrap .spdlbl {{ color:var(--sub); }}
  .readBtn {{ border:1px solid var(--daily); background:var(--daily); color:#fff; border-radius:8px; padding:4px 12px; font-size:12px; cursor:pointer; }}
  .readBtn:hover {{ filter:brightness(1.06); }}
  .readBtn.run {{ background:#dc2626; border-color:#dc2626; }}
  .toggle {{ width:100%; margin-top:8px; border:1px dashed #cbd5e1; background:#fafafa;
    color:#475569; border-radius:8px; padding:6px; font-size:12px; cursor:pointer; }}
  .toggle.ready {{ border-color:var(--accent); color:#b45309; background:#fffbeb; }}
  .toggle:hover {{ filter:brightness(.98); }}
  .detail {{ display:none; margin-top:8px; padding:10px 12px; background:#f8fafc;
    border:1px solid var(--line); border-radius:8px; font-size:12.5px; line-height:1.65; }}
  .detail.open {{ display:block; }}
  .d-row {{ margin-bottom:8px; }}
  .d-row:last-child {{ margin-bottom:0; }}
  .d-k {{ display:inline-block; font-size:11px; font-weight:700; color:#fff; background:var(--daily);
    border-radius:5px; padding:1px 7px; margin-bottom:4px; }}
  .d-v.ipa {{ font-family:"Cambria Math",Georgia,serif; color:#be123c; font-size:14px; }}
  .d-list {{ margin:2px 0 0; padding-left:18px; }}
  .d-list li {{ margin-bottom:3px; }}
  .dn {{ color:var(--sub); }}
  .d-occ {{ color:#7c3aed; font-weight:600; }}
  .d-empty {{ color:var(--sub); font-size:12px; }}
  footer {{ text-align:center; color:var(--sub); font-size:12px; padding:18px; }}
  .pagenav {{ display:flex; gap:8px; flex-wrap:wrap; }}
  .pagenav a {{ text-decoration:none; font-size:13px; color:#fff; border:1px solid rgba(255,255,255,.55); border-radius:999px; padding:6px 14px; font-weight:600; transition:.15s; background:rgba(255,255,255,.15); }}
  .pagenav a:hover {{ background:rgba(255,255,255,.32); border-color:#fff; }}
</style>
</head>
<body>
<header>
  <div class="htitle">
    <h1>旅游 + 日常英语 · {total} 句范式总览</h1>
    <p>每天 5 句随机推送 · 每 30 天 +50 新句（{total}→{total+50}→{total+100}…）· 点击 ▶ 听原声（en-US-Aria 真人音色）· 点「🔤 发音详情」看完整音变标注</p>
  </div>
  <nav class="pagenav">
    <a href="index.html">🏠 首页</a>
    <a href="review.html">📚 已学回顾</a>
    <a href="calendar.html">📅 日历</a>
  </nav>
</header>
<details class="legend-box">
  <summary>🔤 发音详情说明（覆盖 8 类语流音变 · 点击展开/收起）</summary>
  <div class="legend-body">
    🔤 <b>发音详情</b> 覆盖：连读 linking · 同化 assimilation（d+j→dʒ / t+j→tʃ / s+j→ʃ）· 滑音 glide · 清辅音浊化（t→d / p→b / k→g）· 失去爆破 / 不完全爆破 · 闪音 / 弹音（better→/bɛɾɚ/）· 弱读（the→/ðə/）· 缩读（I'd=I would）。已推送句（#1–#5）含完整标注，其余将在学习时自动生成。
  </div>
</details>
  {stats_html}
  <div class="bar">
    <button class="tbtn" id="filterToggle" onclick="toggleFilters()">🔍 筛选条件（已折叠 ▸）</button>
    <div class="filtersBody collapsed" id="filtersBody">
      <div class="grp">
        <button class="tbtn on" data-theme="all">全部</button>
        <button class="tbtn" data-theme="travel">旅游</button>
        <button class="tbtn" data-theme="daily">日常</button>
      </div>
      <div class="grp" id="learnGroup">
        <button class="tbtn on" data-learn="all">全状态</button>
        <button class="tbtn" data-learn="yes">已学</button>
        <button class="tbtn" data-learn="no">未学</button>
      </div>
      <div class="grp" id="cats">{catbtns}</div>
    </div>
    <button class="tbtn" id="expandAll">🔤 展开全部发音详情</button>
    <button class="tbtn" id="syncBtn">🔄 同步掌握度</button>
    <label class="speedWrap">语速(批量预设) <select id="speedSel" class="tbtn" title="设为统一语速并应用到全部句子">
      <option value="1">1.0x</option>
      <option value="0.75">0.75x</option>
      <option value="0.5">0.5x</option>
    </select></label>
    <span class="count" id="count"></span>
  </div>
<div class="grid" id="grid">{cards}</div>
<footer>共 {len(S)} 句 · 数据来自 master.json · 生词已注音标 · 发音详情随每日推送逐步补全</footer>
<script>
  const grid = document.getElementById('grid');
  const cards = [...grid.children];
  const countEl = document.getElementById('count');
  let themeFilter = 'all';
  let catFilter = 'all';
  let learnFilter = 'all';
  function apply() {{
    let n = 0;
    cards.forEach(c => {{
      const okT = themeFilter === 'all' || c.dataset.theme === themeFilter;
      const okC = catFilter === 'all' || c.dataset.cat === catFilter;
      const okL = learnFilter === 'all' || c.dataset.learned === learnFilter;
      const show = okT && okC && okL;
      c.style.display = show ? '' : 'none';
      if (show) n++;
    }});
    countEl.textContent = '显示 ' + n + ' / ' + cards.length + ' 句';
    updateStats();
  }}
  function updateStats() {{
    let nL = 0, sumL = 0, nVis = 0, sumVis = 0;
    cards.forEach(c => {{
      const okT = themeFilter === 'all' || c.dataset.theme === themeFilter;
      const okC = catFilter === 'all' || c.dataset.cat === catFilter;
      const okL = learnFilter === 'all' || c.dataset.learned === learnFilter;
      if (!(okT && okC && okL)) return;
      nVis++;
      const m = parseInt(c.dataset.mastery || '0', 10);
      sumVis += m;
      if (c.dataset.learned === 'yes') {{ nL++; sumL += m; }}
    }});
    const avgLearned = nL ? (sumL / nL) : 0;
    const pct = nVis ? Math.round(sumVis / nVis / 5 * 100) : 0;
    document.getElementById('stLearned').textContent = nL;
    document.getElementById('stTotal').textContent = nVis;
    document.getElementById('stAvg').textContent = avgLearned.toFixed(1);
    const bar = document.getElementById('stBar');
    bar.style.width = pct + '%';
    bar.style.background = pct >= 80 ? '#16a34a' : (pct >= 40 ? '#d97706' : '#dc2626');
    document.getElementById('stPct').textContent = '总掌握度 ' + pct + '%';
  }}
  document.querySelectorAll('.tbtn[data-theme]').forEach(b => b.onclick = () => {{
    document.querySelectorAll('.tbtn[data-theme]').forEach(x => x.classList.remove('on'));
    b.classList.add('on'); themeFilter = b.dataset.theme; apply();
  }});
  document.querySelectorAll('#learnGroup .tbtn').forEach(b => b.onclick = () => {{
    document.querySelectorAll('#learnGroup .tbtn').forEach(x => x.classList.remove('on'));
    b.classList.add('on'); learnFilter = b.dataset.learn; apply();
  }});
  document.querySelectorAll('.fbtn').forEach(b => b.onclick = () => {{
    if (b.classList.contains('on')) {{ b.classList.remove('on'); catFilter = 'all'; }}
    else {{ document.querySelectorAll('.fbtn').forEach(x => x.classList.remove('on')); b.classList.add('on'); catFilter = b.dataset.cat; }}
    apply();
  }});
  const ft = document.getElementById('filterToggle');
  const fb = document.getElementById('filtersBody');
  function setFilterCollapsed(c) {{
    fb.classList.toggle('collapsed', c);
    ft.textContent = c ? '🔍 筛选条件（已折叠 ▸）' : '🔍 筛选条件（展开中 ▾）';
    try {{ localStorage.setItem('vocab_filters_collapsed', c ? '1' : '0'); }} catch(e){{}}
  }}
  function toggleFilters() {{ setFilterCollapsed(!fb.classList.contains('collapsed')); }}
  ft.onclick = toggleFilters;
  try {{ const fcol = localStorage.getItem('vocab_filters_collapsed');
    setFilterCollapsed(fcol === null ? true : fcol === '1'); }} catch(e){{ setFilterCollapsed(true); }}
  const ea = document.getElementById('expandAll');
  ea.onclick = () => {{
    const open = !ea.classList.contains('on');
    ea.classList.toggle('on', open);
    ea.textContent = open ? '🔤 收起全部发音详情' : '🔤 展开全部发音详情';
    document.querySelectorAll('.detail').forEach(d => d.classList.toggle('open', open));
  }};
  const API_PORT = 3279;
  async function apiFetch(path){{
    for(const b of ['', 'http://127.0.0.1:'+API_PORT]){{
      try{{ const r = await fetch(b+path); if(r && r.ok) return r; }}catch(e){{}}
    }}
    return null;
  }}
  function renderBar(card, m){{
    const lvl = m>=5?'lvl-green':(m>=3?'lvl-yellow':'lvl-red');
    const seg = Array.from({{length:5}},(_,i)=>`<i class="${{i<m?'on':''}}"></i>`).join('');
    const mw = card.querySelector('.mwrap'); const mb = card.querySelector('.mbar'); const mn = card.querySelector('.mnum');
    if(mw) mw.className = 'mwrap '+lvl;
    if(mb){{ mb.className='mbar '+lvl; mb.innerHTML=seg; }}
    if(mn) mn.textContent = m+'/5';
    card.dataset.mastery = m;
  }}
  async function syncMastery(){{
    const r = await apiFetch('/api/mastery');
    if(!r) return false;
    const j = await r.json();
    const map = {{}}; (j.sentences||[]).forEach(s=> map[s.id]=s.mastery);
    cards.forEach(c=>{{
      const sid = c.querySelector('.sid'); const id = sid?parseInt(sid.textContent.replace('#',''),10):null;
      if(id!=null && (id in map)) renderBar(c, map[id]);
    }});
    updateStats();
    return true;
  }}
  const sb = document.getElementById('syncBtn');
  if(sb) sb.onclick = async () => {{
    const ok = await syncMastery();
    sb.textContent = ok?'🔄 已同步 ✓':'🔄 服务未连接';
    setTimeout(()=>sb.textContent='🔄 同步掌握度',1600);
  }};
  syncMastery();
  setInterval(syncMastery, 15000);
  // ===== 每句独立语速 + 循环跟读 =====
  function bindCard(card) {{
    const sidEl = card.querySelector('.sid');
    const sid = sidEl ? sidEl.textContent.replace('#','') : '';
    const repsSel = card.querySelector('.repsSel');
    const spdSel = card.querySelector('.spdSel');
    const readBtn = card.querySelector('.readBtn');
    if(!spdSel || !readBtn) return;
    let defSp = '1';
    try {{ defSp = localStorage.getItem('vocab_speed') || '1'; }} catch(e){{}}
    let curSpeed = defSp;
    try {{ curSpeed = localStorage.getItem('vocab_speed_'+sid) || defSp; }} catch(e){{}}
    spdSel.value = curSpeed;
    spdSel.onchange = () => {{
      curSpeed = spdSel.value;
      try {{ localStorage.setItem('vocab_speed_'+sid, curSpeed); }} catch(e){{}}
    }};
    let speaking = false, remain = 0;
    function getAudio() {{
      let a = card.querySelector('audio.mta');
      if(!a){{ a = document.createElement('audio'); a.className='mta'; a.preload='none'; a.src='audio/s'+sid+'.mp3'; card.appendChild(a); }}
      return a;
    }}
    function speakRep() {{
      if(!speaking){{ stop(); return; }}
      const a = getAudio();
      a.playbackRate = parseFloat(curSpeed) || 1;
      a.onended = () => {{ remain--; if(remain > 0 && speaking) speakRep(); else stop(); }};
      a.onerror = () => {{ stop(); }};
      try {{ a.currentTime = 0; }} catch(e){{}}
      a.play().catch(() => {{ stop(); }});
    }}
    function stop() {{
      speaking = false; remain = 0;
      const a = card.querySelector('audio.mta');
      if(a){{ try {{ a.pause(); a.currentTime = 0; }} catch(e){{}} }}
      readBtn.textContent = '▶ 开始';
      readBtn.classList.remove('run');
    }}
    readBtn.addEventListener('click', () => {{
      if(speaking) {{ stop(); return; }}
      const reps = parseInt(repsSel ? repsSel.value : '3', 10) || 3;
      speaking = true; remain = reps;
      readBtn.textContent = '⏹ 停止';
      readBtn.classList.add('run');
      speakRep();
    }});
  }}
  cards.forEach(bindCard);

  const speedSel = document.getElementById('speedSel');
  function applySpeed(v) {{
    cards.forEach(c => {{
      const s = c.querySelector('.spdSel');
      if(s) s.value = v;
      const se = c.querySelector('.sid'); const sid = se ? se.textContent.replace('#','') : '';
      try {{ if(sid) localStorage.setItem('vocab_speed_'+sid, v); }} catch(e){{}}
    }});
    try {{ localStorage.setItem('vocab_speed', v); }} catch(e){{}}
  }}
  try {{ speedSel.value = localStorage.getItem('vocab_speed') || '1'; }} catch(e){{ speedSel.value = '1'; }}
  speedSel.onchange = () => applySpeed(speedSel.value);
  apply();
</script>
</body>
</html>'''

with open("master.html", "w", encoding="utf-8") as f:
    f.write(html)
print("master.html written, sentences =", len(S))
