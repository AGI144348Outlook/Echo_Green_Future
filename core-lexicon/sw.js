// Core Lexicon service worker: cache-first app shell + bundled Pyodide, so it runs fully offline.
const CACHE = 'core-lexicon-v14';
const SHELL = [
  './', 'index.html', 'words.json', 'manifest.webmanifest',
  'iching.json', 'latin.json', 'hebrew.json', 'chinese.json', 'pos.json', 'math_formulas.json', 'math_axioms.json', 'math_symbols.json', 'sci_laws.json', 'sci_principles.json', 'sci_symbols.json', 'codices.json', 'characters.json', 'realms.json', 'documentation.json', 'docs/ep7.json', 'icon.svg', 'icon-192.png', 'icon-512.png',
  'pyodide/pyodide.js', 'pyodide/pyodide.asm.js', 'pyodide/pyodide.asm.wasm',
  'pyodide/python_stdlib.zip', 'pyodide/pyodide-lock.json'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(caches.match(e.request, {ignoreSearch: true}).then(hit => hit || fetch(e.request).then(res => {
    if (res.ok && new URL(e.request.url).origin === location.origin) {
      const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy));
    }
    return res;
  })));
});
