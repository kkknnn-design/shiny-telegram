const CACHE = 'daily-album-white-v2';
const ROOT = new URL('./', self.location.href);
const CORE = ['album.html', 'album.webmanifest', 'album-assets/icon.svg', 'album-assets/icon-180.png', 'album-assets/icon-192.png', 'album-assets/icon-512.png'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(CORE.map(p => new URL(p,ROOT).href))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('daily-album-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if(event.request.method !== 'GET' || url.origin !== ROOT.origin) return;
  if(url.href !== new URL('album.html',ROOT).href && url.href !== new URL('album.webmanifest',ROOT).href && !url.pathname.startsWith(new URL('album-assets/',ROOT).pathname)) return;
  if(event.request.mode === 'navigate') {
    event.respondWith(fetch(event.request).then(response => {
      if(response.ok){const copy=response.clone();event.waitUntil(caches.open(CACHE).then(c=>c.put(event.request,copy)));}
      return response;
    }).catch(() => caches.match(event.request)));
  } else {
    event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
      if(response.ok){const copy=response.clone();event.waitUntil(caches.open(CACHE).then(c=>c.put(event.request,copy)));}
      return response;
    })));
  }
});
