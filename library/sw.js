// 由 tools/build-library.py 生成。书架与公共资源预缓存；阅读过的册在打开时缓存，便于离线阅读。
const CACHE = 'textbook-library-7a357bb2';
const CORE = ["./", "index.html", "manifest.webmanifest", "icon.svg", "library.css?v=7a357bb2", "reader.js?v=7a357bb2", "shelf.js?v=7a357bb2", "fonts/KaTeX_AMS-400-normal.woff2", "fonts/KaTeX_Caligraphic-400-normal.woff2", "fonts/KaTeX_Caligraphic-700-normal.woff2", "fonts/KaTeX_Fraktur-400-normal.woff2", "fonts/KaTeX_Fraktur-700-normal.woff2", "fonts/KaTeX_Main-400-italic.woff2", "fonts/KaTeX_Main-400-normal.woff2", "fonts/KaTeX_Main-700-italic.woff2", "fonts/KaTeX_Main-700-normal.woff2", "fonts/KaTeX_Math-400-italic.woff2", "fonts/KaTeX_Math-700-italic.woff2", "fonts/KaTeX_SansSerif-400-italic.woff2", "fonts/KaTeX_SansSerif-400-normal.woff2", "fonts/KaTeX_SansSerif-700-normal.woff2", "fonts/KaTeX_Script-400-normal.woff2", "fonts/KaTeX_Size1-400-normal.woff2", "fonts/KaTeX_Size2-400-normal.woff2", "fonts/KaTeX_Size3-400-normal.woff2", "fonts/KaTeX_Size4-400-normal.woff2", "fonts/KaTeX_Typewriter-400-normal.woff2"];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('textbook-library-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  const scope = new URL('./', self.registration.scope).pathname;
  if (!url.pathname.startsWith(scope)) return;
  const put = res => { if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); } return res; };
  if (req.mode === 'navigate' || url.pathname.endsWith('.html') || url.pathname === scope) {
    e.respondWith(fetch(req).then(put).catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || caches.match('index.html'))));
  } else {
    e.respondWith(caches.match(req).then(r => r || fetch(req).then(put)));
  }
});
