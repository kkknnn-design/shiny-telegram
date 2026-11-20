// 教材书架 · 首页脚本：继续阅读、阅读进度、跨书标题搜索、主题切换。
(function () {
  'use strict';
  var BOOKS = JSON.parse(document.getElementById('books-data').textContent);
  var $ = function (s) { return document.querySelector(s); };
  var root = document.documentElement;
  function load(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // 主题：auto → light → sepia → dark 循环
  var settings = load('lib-settings', {});
  var THEMES = ['auto', 'light', 'sepia', 'dark'], NAMES = { auto: '跟随系统', light: '浅色', sepia: '护眼', dark: '深色' };
  function applyTheme() { root.setAttribute('data-theme', settings.theme || 'auto'); $('#themeBtn').setAttribute('aria-label', '主题：' + NAMES[settings.theme || 'auto']); $('#themeBtn').title = NAMES[settings.theme || 'auto']; }
  $('#themeBtn').addEventListener('click', function () {
    var i = THEMES.indexOf(settings.theme || 'auto');
    settings.theme = THEMES[(i + 1) % THEMES.length]; save('lib-settings', settings); applyTheme();
  });
  applyTheme();

  // 进度条与继续阅读
  var latest = null;
  BOOKS.forEach(function (b) {
    var p = load('lib-pos-' + b.code, null);
    var bar = document.querySelector('[data-bar="' + b.code + '"]');
    var pct = document.querySelector('[data-pct="' + b.code + '"]');
    if (p && p.pct > 0.005) {
      if (bar) bar.style.width = (p.pct * 100).toFixed(1) + '%';
      if (pct) pct.textContent = '已读 ' + Math.round(p.pct * 100) + '%';
      if (!latest || p.t > latest.p.t) latest = { b: b, p: p };
    }
  });
  if (latest) {
    var c = $('#continue');
    c.href = latest.b.href;
    c.querySelector('.mini').style.background = latest.b.color;
    c.querySelector('.b').textContent = latest.b.title;
    c.querySelector('.c').textContent = (latest.p.ch || '') + ' · ' + Math.round(latest.p.pct * 100) + '%';
    c.hidden = false;
  }

  // 搜索：书名、学习路线、章节标题
  var input = $('#q'), results = $('#results'), shelf = $('#shelf');
  function mark(text, q) {
    var i = text.toLowerCase().indexOf(q.toLowerCase());
    if (i < 0) return esc(text);
    return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + q.length)) + '</mark>' + esc(text.slice(i + q.length));
  }
  function search() {
    var q = input.value.trim();
    if (!q) { results.hidden = true; shelf.hidden = false; return; }
    var out = [], ql = q.toLowerCase();
    BOOKS.forEach(function (b) {
      if ((b.title + b.sub + b.route).toLowerCase().indexOf(ql) >= 0) out.push('<li><a href="' + b.href + '"><div class="rb">教材</div><div class="rh">' + mark(b.title, q) + '</div></a></li>');
      b.toc.forEach(function (h) {
        if (h[1].toLowerCase().indexOf(ql) >= 0) out.push('<li><a href="' + b.href + '#' + h[0] + '"><div class="rb">' + esc(b.title) + '</div><div class="rh">' + mark(h[1], q) + '</div></a></li>');
      });
    });
    results.innerHTML = out.length ? out.slice(0, 80).join('') : '<li class="empty">没有找到“' + esc(q) + '”相关的章节</li>';
    results.hidden = false; shelf.hidden = true;
  }
  input.addEventListener('input', search);
  search();

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    navigator.serviceWorker.register('sw.js').catch(function () {});
  }
})();
