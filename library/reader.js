// 教材书架 · 阅读页脚本：目录抽屉、阅读设置、进度记忆、离线缓存。
(function () {
  'use strict';
  var root = document.documentElement;
  var code = root.getAttribute('data-book');
  var POS_KEY = 'lib-pos-' + code;
  var SET_KEY = 'lib-settings';
  var $ = function (s) { return document.querySelector(s); };
  var book = $('#book'), bar = $('.topbar'), prog = $('#prog'), curCh = $('#curCh');
  var drawer = $('#toc'), sheet = $('#settings'), scrim = $('#scrim'), toast = $('#toast'), totop = $('#totop');

  function load(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  // ---------- 设置 ----------
  var SIZES = [15, 16, 17, 18, 20, 22];
  var settings = load(SET_KEY, {});
  function applySettings() {
    root.setAttribute('data-theme', settings.theme || 'auto');
    root.setAttribute('data-font', settings.font || 'serif');
    root.style.setProperty('--fs', (settings.size || 17) + 'px');
    sheet.querySelectorAll('[data-k]').forEach(function (b) {
      var k = b.getAttribute('data-k'), v = b.getAttribute('data-v');
      var cur = k === 'theme' ? (settings.theme || 'auto') : k === 'font' ? (settings.font || 'serif') : null;
      if (cur !== null) b.classList.toggle('on', cur === v);
    });
    $('#sizeVal').textContent = settings.size || 17;
  }
  sheet.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var anchor = currentAnchor();
    var k = b.getAttribute('data-k'), v = b.getAttribute('data-v');
    if (k === 'theme' || k === 'font') settings[k] = v;
    if (k === 'size') {
      var i = SIZES.indexOf(settings.size || 17); if (i < 0) i = 2;
      i = Math.max(0, Math.min(SIZES.length - 1, i + (v === '+' ? 1 : -1)));
      settings.size = SIZES[i];
    }
    save(SET_KEY, settings); applySettings();
    if (k === 'size' || k === 'font') { restoreAnchor(anchor); fitInlineMath(); }
  });

  // ---------- 抽屉与面板 ----------
  function closeAll() { drawer.classList.remove('on'); sheet.classList.remove('on'); scrim.classList.remove('on'); }
  function open(el) {
    closeAll(); el.classList.add('on'); scrim.classList.add('on');
    if (el === drawer) { var c = drawer.querySelector('a.cur'); if (c) { var ol = drawer.querySelector('ol'); ol.scrollTop = c.offsetTop - ol.clientHeight / 2; } }
  }
  $('#tocBtn').addEventListener('click', function () { open(drawer); });
  $('#setBtn').addEventListener('click', function () { open(sheet); });
  scrim.addEventListener('click', closeAll);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(); });
  drawer.addEventListener('click', function (e) { if (e.target.closest('a')) closeAll(); });
  totop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  // ---------- 点图放大：全屏查看插图，可双指缩放、横向滑动 ----------
  var viewer = document.createElement('div');
  viewer.className = 'viewer'; viewer.setAttribute('role', 'dialog'); viewer.setAttribute('aria-label', '查看插图');
  viewer.innerHTML = '<div class="vbody"><img alt=""></div><div class="vcap"></div><button class="vclose" aria-label="关闭">×</button>';
  document.body.appendChild(viewer);
  var vimg = viewer.querySelector('img'), vcap = viewer.querySelector('.vcap');
  function closeViewer() { viewer.classList.remove('on'); document.documentElement.classList.remove('noscroll'); }
  book.addEventListener('click', function (e) {
    var img = e.target.closest('img'); if (!img) return;
    vimg.src = img.currentSrc || img.src; vimg.alt = img.alt;
    var cap = img.closest('figure'); cap = cap && cap.querySelector('figcaption');
    vcap.textContent = cap ? cap.textContent : img.alt;
    viewer.classList.add('on'); document.documentElement.classList.add('noscroll');
  });
  viewer.addEventListener('click', function (e) { if (e.target === viewer || e.target.closest('.vclose') || e.target.classList.contains('vbody')) closeViewer(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeViewer(); });

  // ---------- 进度与当前章节 ----------
  var heads = Array.prototype.slice.call(book.querySelectorAll('h2[id],h3[id]'));
  var links = {};
  drawer.querySelectorAll('ol a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  var blocks = book.children;
  var lastY = window.scrollY, curId = null, userScrolled = false;

  function barH() { return bar.getBoundingClientRect().bottom > 0 ? bar.offsetHeight : 0; }
  function currentAnchor() {
    var top = barH() + 4;
    for (var i = 0; i < blocks.length; i++) {
      var r = blocks[i].getBoundingClientRect();
      if (r.bottom > top) return { i: i, f: r.height ? Math.max(0, (top - r.top) / r.height) : 0 };
    }
    return { i: 0, f: 0 };
  }
  function restoreAnchor(a) {
    var el = blocks[a.i]; if (!el) return;
    var r = el.getBoundingClientRect();
    window.scrollTo(0, window.scrollY + r.top + r.height * (a.f || 0) - (bar.offsetHeight + 4));
  }
  function heading() {
    var top = bar.offsetHeight + 24, h = null;
    for (var i = 0; i < heads.length; i++) { if (heads[i].getBoundingClientRect().top <= top) h = heads[i]; else break; }
    return h;
  }
  function chapterOf(h) {
    if (!h) return null;
    if (h.tagName === 'H2') return h;
    for (var i = heads.indexOf(h); i >= 0; i--) if (heads[i].tagName === 'H2') return heads[i];
    return h;
  }
  var saveTimer = 0;
  function onScroll() {
    var y = window.scrollY, max = document.documentElement.scrollHeight - window.innerHeight;
    var pct = max > 0 ? Math.min(1, y / max) : 0;
    prog.style.width = (pct * 100).toFixed(2) + '%';
    if (!drawer.classList.contains('on') && !sheet.classList.contains('on')) {
      if (y > lastY + 6 && y > 120) bar.classList.add('hide');
      else if (y < lastY - 6) bar.classList.remove('hide');
    }
    lastY = y;
    totop.classList.toggle('on', y > window.innerHeight * 2);
    var h = heading(), id = h ? h.id : null;
    if (id !== curId) {
      if (curId && links[curId]) links[curId].classList.remove('cur');
      if (id && links[id]) links[id].classList.add('cur');
      curId = id;
      var ch = chapterOf(h);
      curCh.textContent = ch ? ch.textContent : '封面';
    }
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      var a = currentAnchor(), ch = chapterOf(heading());
      save(POS_KEY, { i: a.i, f: +a.f.toFixed(3), pct: +pct.toFixed(4), ch: ch ? ch.textContent : '', t: Date.now() });
    }, 400);
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; onScroll(); }); }
  }, { passive: true });
  ['touchstart', 'wheel', 'keydown'].forEach(function (ev) {
    window.addEventListener(ev, function () { userScrolled = true; }, { passive: true, once: true });
  });

  // ---------- 行内长公式：超出版心时改为可横向滑动 ----------
  function fitInlineMath() {
    var w = book.clientWidth - 36;
    book.querySelectorAll('.k-scroll').forEach(function (s) { s.classList.remove('k-scroll'); });
    book.querySelectorAll('p .katex, li .katex, td .katex').forEach(function (k) {
      if (k.closest('.katex-display')) return;
      if (k.offsetWidth > w) k.classList.add('k-scroll');
    });
  }

  function showToast(text, action, fn) {
    toast.innerHTML = '';
    var s = document.createElement('span'); s.textContent = text; toast.appendChild(s);
    if (action) {
      var b = document.createElement('button'); b.textContent = action;
      b.addEventListener('click', function () { fn(); toast.classList.remove('on'); });
      toast.appendChild(b);
    }
    toast.classList.add('on');
    setTimeout(function () { toast.classList.remove('on'); }, 4500);
  }

  // ---------- 启动 ----------
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  applySettings();
  var pos = load(POS_KEY, null);
  function restore() {
    if (location.hash) { var t = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (t) t.scrollIntoView(); return; }
    if (pos && pos.i > 2) restoreAnchor(pos);
  }
  // 程序性跳转不应触发“下滑隐藏顶栏”
  var restoreRaw = restore;
  restore = function () { restoreRaw(); lastY = window.scrollY; bar.classList.remove('hide'); };
  restore();
  fitInlineMath();
  onScroll();
  if (pos && pos.i > 2 && !location.hash) {
    showToast('已回到上次读到的位置' + (pos.ch ? '：' + pos.ch : ''), '从头读', function () { window.scrollTo(0, 0); });
  }
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { if (!userScrolled) restore(); fitInlineMath(); onScroll(); });
  }
  var rt = 0;
  window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(fitInlineMath, 200); });

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    navigator.serviceWorker.register('sw.js').catch(function () {});
  }
})();
