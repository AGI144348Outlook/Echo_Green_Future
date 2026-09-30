const CACHE = 'echo-dev-suite-shell-v2';
const SHELL = ['./','index.html','manifest.webmanifest','js/app.js','js/python-worker.js','python/algorithm_matrix.py','icons/icon-192.png','icons/icon-512.png'];
self.addEventListener('install', event => event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL))));
self.addEventListener('activate', event => event.waitUntil(self.clients.claim()));
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET' || new URL(event.request.url).origin !== self.location.origin) return;
  event.respondWith(fetch(event.request).catch(() => caches.match(event.request).then(response => response || Response.error())));
});
