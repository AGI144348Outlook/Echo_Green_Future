/* Service worker: app shell + ECHO package precached; the Pyodide runtime from
   jsDelivr is cached the first time it loads, so later starts work offline.
   Bump VERSION whenever any shipped file changes. */
const VERSION = 'echo-pwa-0.1.0';
const SHELL = ['./', './index.html', './manifest.webmanifest', './css/app.css',
  './js/store.js', './js/nve.js', './js/renderer.js', './js/widgets.js', './js/io.js',
  './js/panels.js', './js/bridge.js', './js/app.js', './icons/icon-192.png', './icons/icon-512.png',
  './echo/manifest.json'];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(VERSION);
    await cache.addAll(SHELL);
    try {
      const man = await (await fetch('./echo/manifest.json', { cache: 'no-cache' })).json();
      await cache.addAll(man.files.map(f => './' + f + '?v=' + man.version));
    } catch (e) { /* package files will be cached on first use */ }
    self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== VERSION) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;                 // MCW POSTs go straight to the network
  const url = new URL(req.url);
  const pyodide = url.hostname === 'cdn.jsdelivr.net' && url.pathname.startsWith('/pyodide/');
  const same = url.origin === self.location.origin;
  if (!pyodide && !same) return;
  if (same && url.pathname.endsWith('/echo/manifest.json')) {
    // network first, so a new package version is picked up when online
    event.respondWith(fetch(req).then(res => { put(req, res.clone()); return res; }).catch(() => caches.match(req)));
    return;
  }
  event.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {
    if (res.ok) put(req, res.clone());
    return res;
  }).catch(() => (req.mode === 'navigate' ? caches.match('./index.html') : Response.error()))));
});

function put(req, res) { caches.open(VERSION).then(c => c.put(req, res)).catch(() => {}); }
