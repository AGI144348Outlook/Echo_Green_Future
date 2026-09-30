/* Bridge: the one seam between the JavaScript shell and ECHO's Python runtime.
   Pyodide loads from the jsDelivr CDN (pinned). For local testing a different
   base can be given with ?pyodide=<url-ending-in-slash>. The service worker
   caches the runtime after the first load, so later starts work offline. */
(function (E) {
  'use strict';
  const PYODIDE_VERSION = '0.26.4';
  const qs = new URLSearchParams(location.search);
  const BASE = qs.get('pyodide') || ('https://cdn.jsdelivr.net/pyodide/v' + PYODIDE_VERSION + '/full/');

  const B = E.bridge = {
    ready: false, status: 'idle', detail: '', error: null, py: null, mod: null, identity: null,
    events: new EventTarget(),
    start,
    handle(text, mode, snap) { return call('handle', text, mode, JSON.stringify(snap)); },
    onPresentiate(snap, id) { return call('on_presentiate', JSON.stringify(snap), id); },
    resolve(word) { return call('resolve', word); },
    words() { return call('words'); },
    setOverlay(o) { return call('set_overlay', JSON.stringify(o || {})); },
  };

  function set(status, detail) {
    B.status = status; B.detail = detail || '';
    B.events.dispatchEvent(new CustomEvent('status', { detail: { status, detail: B.detail } }));
  }

  function call(fn, ...args) {
    if (!B.ready) return null;
    try { return JSON.parse(B.mod[fn](...args)); }
    catch (e) { console.error(e); return { outputs: [{ actor: 'echo', kind: 'error', text: 'Runtime error: ' + e.message, refs: [] }], ops: [] }; }
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      if (window.loadPyodide) return resolve();
      const s = document.createElement('script');
      s.src = src; s.onload = resolve;
      s.onerror = () => reject(new Error('could not load ' + src));
      document.head.appendChild(s);
    });
  }

  async function start(config) {
    if (B.status === 'loading') return;
    B.ready = false; B.error = null;
    try {
      set('loading', 'Pyodide runtime');
      await loadScript(BASE + 'pyodide.js');
      const py = await window.loadPyodide({ indexURL: BASE });
      B.py = py;
      set('loading', 'ECHO package');
      const man = await (await fetch('./echo/manifest.json', { cache: 'no-cache' })).json();
      let n = 0;
      for (const f of man.files) {
        const res = await fetch('./' + f + '?v=' + man.version);
        if (!res.ok) throw new Error('missing ' + f + ' (' + res.status + ')');
        const dir = '/home/pyodide/' + f.split('/').slice(0, -1).join('/');
        py.FS.mkdirTree(dir);
        py.FS.writeFile('/home/pyodide/' + f, await res.text());
        set('loading', 'ECHO package ' + (++n) + '/' + man.files.length);
      }
      py.runPython("import sys\nif '/home/pyodide' not in sys.path: sys.path.insert(0, '/home/pyodide')");
      set('loading', 'booting kernel');
      B.mod = py.pyimport('echo.bootstrap.boot');
      const r = JSON.parse(B.mod.boot(JSON.stringify(config || {})));
      B.identity = r.identity;
      B.ready = true;
      set('ready', r.identity.identity);
      return r;
    } catch (e) {
      console.error(e);
      B.error = e.message || String(e);
      set('error', B.error);
      return null;
    }
  }
})(window.ECHO = window.ECHO || {});
