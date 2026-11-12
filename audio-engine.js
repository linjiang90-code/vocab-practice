/* 统一朗读引擎：用 Web Audio API 解码播放，playbackRate 在所有设备（含 iOS Safari）
   都生效。原生 <audio>.playbackRate 在 iOS Safari 会被静默忽略，所以必须用 Web Audio。
   无 Web Audio 时回退到 <audio>（桌面仍有效）。

   关键健壮性（2026-08-19 修正）：
   - 顺序/循环播放不再单纯依赖 onended。部分浏览器（尤其移动端/远程 Edge）在
     程序化连续播放时 onended 经常不触发，导致"只读一句/循环卡住/停止无效"。
   - 改为：每次播放用「缓冲时长 × (1/rate) + 余量」启动一个兜底定时器，
     无论 onended 是否触发，都会准时推进到下一句 / 下一遍 / 触发 onEnd。
   - 每次播放前 ac() 恢复 AudioContext，避免上下文在句间被挂起导致静音。
   依赖：在页面 <script> 之前用 <script src="audio-engine.js"></script> 引入。 */
(function(){
  'use strict';
  var AC = window.AudioContext || window.webkitAudioContext;
  var ctx = null;
  function ac(){
    if(!ctx && AC){ try { ctx = new AC(); } catch(e){ ctx = null; } }
    if(ctx && ctx.state === 'suspended'){ try { ctx.resume(); } catch(e){} }
    return ctx;
  }
  function normId(id){
    id = String(id);
    if(id.charAt(0) === 's') id = id.slice(1);
    return 's' + id;
  }
  // ===== 缓存击穿（2026-11-12 二次加固） =====
  // 企业微信内置浏览器（X5/CEF）会无视 Cache-Control: no-store 缓存 mp3，换音色后
  // 用户仍听到旧声。前一次只在 query 上加 ?v=xxx，实测仍被命中 —— 因为这类内核的
  // 媒体缓存按 URL「路径」建键，query 常被忽略。
  // 现改为**路径级版本段**：audio/b<版本>/s123.mp3。
  //   · 路径与旧版完全不同 -> 任何缓存实现都不可能命中旧副本
  //   · 版本目录在磁盘上真实存在（sync_audio_version.py 用硬链接生成），
  //     所以即使服务端 serve.py 还是旧版、没重启，也能当普通静态文件取到音频
  //   · 服务端新版还会把版本段剥掉映射回 audio/s123.mp3，双保险
  // 版本号不在这里硬编码：直接读本文件 <script src="audio-engine.js?v=xxx"> 的 v 值，
  // 「页面引用」是唯一事实来源，换音色只需 bump 页面上的 v 并生成同名目录。
  var SELF_V = (function(){
    try {
      var s = document.currentScript;
      if(!s || !/audio-engine\.js/.test(s.src || '')){
        var ss = document.getElementsByTagName('script');
        for(var i = ss.length - 1; i >= 0; i--){
          if(/audio-engine\.js/.test(ss[i].src || '')){ s = ss[i]; break; }
        }
      }
      var m = s && /[?&]v=([0-9A-Za-z]+)/.exec(s.src || '');
      return m ? m[1] : '';
    } catch(e){ return ''; }
  })();
  var SEG = 'b' + (SELF_V || 'dev');               // 路径版本段
  var BUST = 'v=' + SEG + Date.now().toString(36); // query 戳（只认 query 的代理也能击穿）
  function urlOf(id){ return 'audio/' + SEG + '/' + normId(id) + '.mp3?' + BUST; }

  var bufCache = {};
  function fetchBuf(url){
    return fetch(url).then(function(r){
      if(!r.ok) throw new Error('HTTP ' + r.status);
      return r.arrayBuffer();
    });
  }
  function decode(id){
    return new Promise(function(resolve, reject){
      if(bufCache[id]){ resolve(bufCache[id]); return; }
      // 先试带版本段的路径；若服务端还是旧版（无 /audio/<段>/ 路由 → 404），
      // 自动回退到扁平路径。这样「页面先更新、服务后重启」的窗口期朗读不会全挂。
      fetchBuf(urlOf(id))
        .catch(function(){ return fetchBuf('audio/' + normId(id) + '.mp3?' + BUST); })
      .then(function(ab){
        var c = ac();
        if(!c){ reject(new Error('no AudioContext')); return; }
        // 同时兼容 promise 与 callback 形式的 decodeAudioData（旧 Safari 仅支持 callback）
        var done = false;
        function ok(dec){ if(done) return; done = true; bufCache[id] = dec; resolve(dec); }
        function err(e){ if(done) return; done = true; reject(e); }
        var p = c.decodeAudioData(ab.slice(0), ok, err);
        if(p && p.then){ p.then(ok, err); }
      }).catch(reject);
    });
  }

  var active = {};   // key -> { src, timer, stop }
  // 代次令牌：解码是异步的，快速连点两句时旧的那句可能在新 stopAll 之后才起播，
  // 用它把「已过期」的起播请求作废，彻底避免两句叠在一起。
  var gen = 0;
  function stopKey(key){
    key = normId(key);              // 归一化：'1'/'s1' 都能命中
    var a = active[key];
    if(a){
      try { if(a.timer) clearTimeout(a.timer); } catch(e){}
      try { a.src.onended = null; } catch(e){}
      try { a.src.stop(); } catch(e){}
      try { a.src.disconnect(); } catch(e){}
      delete active[key];
    }
  }
  // 把页面上「⏹ 停止」的按钮复位（旧的日页没有这层逻辑，靠引擎兜住）
  // keepId：正在开始循环的那一句要保留自己的按钮状态
  function resetRunBtns(keepId){
    var keep = keepId ? 'rb-' + normId(keepId) : null;
    try{
      var bs = document.querySelectorAll('.readBtn.run');
      for(var i=0;i<bs.length;i++){
        if(keep && bs[i].id === keep) continue;
        bs[i].classList.remove('run');
        bs[i].textContent = '▶ 开始';
      }
    }catch(e){}
  }
  function stopAll(keepId){
    gen++;                            // 让还在解码中的旧请求作废
    Object.keys(active).forEach(stopKey);
    stopAllFallback(keepId);
    resetRunBtns(keepId);
  }
  function isActive(id){ return !!active[normId(id)]; }

  // 回退路径（原生 <audio>）也要互斥：只保留 keepId 那条，其余暂停
  function stopAllFallback(keepId){
    try{
      var els = document.querySelectorAll('audio[id^="va-"]');
      for(var i=0;i<els.length;i++){
        if(keepId && els[i].id === 'va-' + normId(keepId)) continue;
        try{ els[i].pause(); els[i].currentTime = 0; }catch(e){}
      }
    }catch(e){}
  }

  // 启动一次播放；onEnd 通过「onended + 时长兜底定时器」双保险触发（只触发一次）
  function startSource(key, id, rate, onEnd, token){
    return decode(id).then(function(buf){
      // 解码期间如果用户已经点了别的句子，这次起播请求直接作废
      if(token !== undefined && token !== gen) return null;
      var c = ac();
      if(!c) throw new Error('no AudioContext');
      var src = c.createBufferSource();
      var r = (rate && rate > 0) ? rate : 1;
      src.buffer = buf;
      src.playbackRate.value = r;
      src.connect(c.destination);
      var done = false;
      function finish(){
        if(done) return; done = true;
        if(onEnd) onEnd();
      }
      src.onended = finish;
      // 兜底定时器：按缓冲真实时长推进，彻底摆脱 onended 不触发的问题
      var durMs = (buf.duration / r) * 1000 + 400;
      var timer = setTimeout(finish, durMs);
      active[key] = { src: src, timer: timer, stop: function(){ stopKey(key); } };
      src.start(0);
      return src;
    });
  }

  function fallbackPlay(id, rate){
    var realId = normId(id);
    stopAllFallback(realId);            // 互斥：先停掉其它正在播的 <audio>
    var a = document.getElementById('va-' + realId);
    if(!a){
      a = document.createElement('audio');
      a.id = 'va-' + realId;
      a.preload = 'none';
      (document.body || document.documentElement).appendChild(a);
    }
    // 回退路径用扁平 URL（一定存在，不依赖服务端版本段路由）；query 戳仍然生效
    a.src = 'audio/' + realId + '.mp3?' + BUST;
    a.playbackRate = (rate && rate > 0) ? rate : 1;
    try { a.currentTime = 0; } catch(e){}
    a.play().catch(function(){});
    return a;
  }

  // 播放一次（可选 onEnd 回调，用于顺序播放）
  function play(id, rate, onEnd){
    var key = normId(id);
    // 互斥播放：任何一句开始播放，都要先停掉其它正在播的句子（含循环中的）
    stopAll();
    var my = gen;
    ac();                              // 在用户手势内创建/恢复 AudioContext
    if(!AC) return fallbackPlay(id, rate);
    return startSource(key, id, rate, onEnd, my).catch(function(){
      return fallbackPlay(id, rate);
    });
  }

  // 循环 reps 次；每轮结束触发 onTick(n)，全部结束触发 onEnd
  function loop(id, rate, reps, cb){
    rate = (rate && rate > 0) ? rate : 1;
    reps = reps || 1;
    var key = normId(id);
    ac();
    if(!AC){ return fallbackPlay(id, rate); }   // 无 Web Audio 时退化为单次播放
    // 互斥：开始循环前先停掉其它句子，避免两句混在一起（保留本句按钮状态）
    stopAll(key);
    var my = gen;
    var n = 0;
    function step(){
      startSource(key, id, rate, function(){
        if(my !== gen) return;          // 已被别的播放取代，不再续读
        n++;
        if(cb && cb.onTick) cb.onTick(n);
        if(n < reps){ step(); }
        else { if(cb && cb.onEnd) cb.onEnd(); delete active[key]; }
      }, my).catch(function(){ if(cb && cb.onEnd) cb.onEnd(); });
    }
    step();
  }

  window.VocabAudio = {
    play: play,
    loop: loop,
    stopId: stopKey,
    stopAll: stopAll,
    isActive: isActive
  };
})();
