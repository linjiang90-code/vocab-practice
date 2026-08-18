/* 统一朗读引擎：用 Web Audio API 解码播放，playbackRate 在所有设备（含 iOS Safari）
   都生效。原生 <audio>.playbackRate 在 iOS Safari 会被静默忽略，所以必须用 Web Audio。
   无 Web Audio 时回退到 <audio>（桌面仍有效）。
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
  function urlOf(id){ return 'audio/' + normId(id) + '.mp3'; }

  var bufCache = {};
  function decode(id){
    return new Promise(function(resolve, reject){
      if(bufCache[id]){ resolve(bufCache[id]); return; }
      fetch(urlOf(id)).then(function(r){
        if(!r.ok) throw new Error('HTTP ' + r.status);
        return r.arrayBuffer();
      }).then(function(ab){
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

  var active = {};   // key -> { src, stop }
  function stopKey(key){
    key = normId(key);              // 归一化：'1'/'s1' 都能命中
    var a = active[key];
    if(a){
      try { a.src.onended = null; } catch(e){}
      try { a.src.stop(); } catch(e){}
      try { a.src.disconnect(); } catch(e){}
      delete active[key];
    }
  }
  function stopAll(){ Object.keys(active).forEach(stopKey); }
  function isActive(id){ return !!active[normId(id)]; }

  function startSource(key, id, rate, onEnd){
    return decode(id).then(function(buf){
      var c = ac();
      var src = c.createBufferSource();
      src.buffer = buf;
      src.playbackRate.value = (rate && rate > 0) ? rate : 1;
      src.connect(c.destination);
      if(onEnd){ src.onended = onEnd; }
      active[key] = { src: src, stop: function(){ stopKey(key); } };
      src.start(0);
      return src;
    });
  }

  function fallbackPlay(id, rate){
    var realId = normId(id);
    var a = document.getElementById('va-' + realId);
    if(!a){
      a = document.createElement('audio');
      a.id = 'va-' + realId;
      a.preload = 'none';
      a.src = urlOf(id);
      (document.body || document.documentElement).appendChild(a);
    }
    a.playbackRate = (rate && rate > 0) ? rate : 1;
    try { a.currentTime = 0; } catch(e){}
    a.play().catch(function(){});
    return a;
  }

  // 播放一次（可选 onEnd 回调，用于顺序播放）
  function play(id, rate, onEnd){
    var key = normId(id);
    stopKey(key);
    ac();                              // 在用户手势内创建/恢复 AudioContext
    if(!AC) return fallbackPlay(id, rate);
    return startSource(key, id, rate, onEnd).catch(function(){
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
    stopKey(key);
    var n = 0;
    function step(){
      startSource(key, id, rate, null).then(function(src){
        src.onended = function(){
          n++;
          if(cb && cb.onTick) cb.onTick(n);
          if(n < reps){ step(); }
          else { if(cb && cb.onEnd) cb.onEnd(); delete active[key]; }
        };
      }).catch(function(){ if(cb && cb.onEnd) cb.onEnd(); });
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
