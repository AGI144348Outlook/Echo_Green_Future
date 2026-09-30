/* Host shell: standalone now, mountable in the larger PWA later.
   Human <-> Notebook I/O <-> Shared Canvas <-> ECHO, all through one store. */
(function (E) {
  'use strict';
  const S = E.store, W = E.widgets, IO = E.io, B = E.bridge;
  const TOOLBAR = 48;
  const $ = s => document.querySelector(s);
  const svg = () => document.getElementById('canvas');

  const App = E.app = {
    settings: { endpoint: '' }, outbox: [], instanceId: null, overlay: {},
    relateMode: false, relateFirst: null, multi: false,
    send, presentiate, focusWord, toast, persistIO, saveSettings, flushOutbox,
    exportJSON, importJSON, saveLayout, restoreLayout, wipe, bootRuntime,
  };

  // ---------- persistence -------------------------------------------------
  let saveT = null, ioT = null, layoutT = null;
  function scheduleSave() {
    clearTimeout(saveT);
    saveT = setTimeout(() => E.nve.set('canvas', { state: S.state, log: S.log.slice(-2000), view: S.view }), 400);
  }
  function persistIO() { clearTimeout(ioT); ioT = setTimeout(() => E.nve.set('io', IO.history.slice(-150)), 600); }
  function saveSettings() { E.nve.set('settings', App.settings); }
  function autosaveLayout() { clearTimeout(layoutT); layoutT = setTimeout(() => E.nve.set('layout:auto', W.serialize()), 300); }
  function saveLayout() { E.nve.set('layout:saved', W.serialize()); W.dispatch({ op: 'SAVE_LAYOUT' }); toast('Layout saved'); }
  async function restoreLayout() {
    const l = await E.nve.get('layout:saved');
    if (!l) { toast('No saved layout yet'); return; }
    W.restore(l); W.dispatch({ op: 'RESTORE_LAYOUT' }); toast('Layout restored');
  }

  // ---------- geometry ------------------------------------------------------
  function dockTop() {
    let top = window.innerHeight;
    W.items.forEach(w => { if (w.docked && !w.maximized && w.el) top = Math.min(top, w.el.getBoundingClientRect().top); });
    return top;
  }
  function visibleCenterWorld() {
    const v = S.view, cx = window.innerWidth / 2, cy = (TOOLBAR + dockTop()) / 2;
    const r = svg().getBoundingClientRect();
    return { x: (cx - r.left - v.x) / v.scale, y: (cy - r.top - v.y) / v.scale };
  }
  function screenToWorld(clientX, clientY) {
    const r = svg().getBoundingClientRect(), v = S.view;
    return { x: (clientX - r.left - v.x) / v.scale, y: (clientY - r.top - v.y) / v.scale };
  }
  function worldToScreen(p) {
    const r = svg().getBoundingClientRect(), v = S.view;
    return { x: p.x * v.scale + v.x + r.left, y: p.y * v.scale + v.y + r.top };
  }
  function centerOn(m) {
    const r = svg().getBoundingClientRect();
    const cx = window.innerWidth / 2 - r.left, cy = (TOOLBAR + dockTop()) / 2 - r.top;
    S.view.x = cx - m.x * S.view.scale; S.view.y = cy - m.y * S.view.scale;
    E.renderer.render(); scheduleSave();
  }
  function fitAll() {
    const ms = Object.values(S.state.manifestations);
    if (!ms.length) { S.view = { x: 0, y: 0, scale: 1 }; E.renderer.render(); return; }
    const r = svg().getBoundingClientRect();
    const minX = Math.min(...ms.map(m => m.x)) - 50, maxX = Math.max(...ms.map(m => m.x)) + 50;
    const minY = Math.min(...ms.map(m => m.y)) - 50, maxY = Math.max(...ms.map(m => m.y)) + 50;
    const availW = window.innerWidth, availH = Math.max(120, dockTop() - TOOLBAR);
    const scale = Math.max(0.3, Math.min(1.2, availW / (maxX - minX), availH / (maxY - minY)));
    S.view.scale = scale;
    S.view.x = (availW - (maxX - minX) * scale) / 2 - minX * scale - r.left;
    S.view.y = TOOLBAR + (availH - (maxY - minY) * scale) / 2 - minY * scale - r.top;
    E.renderer.render(); scheduleSave();
  }
  function ensureVisible(ids) {
    const top = TOOLBAR, bottom = dockTop();
    const off = ids.map(id => S.state.manifestations[id]).filter(Boolean).some(m => {
      const p = worldToScreen(m);
      return p.x < 20 || p.x > window.innerWidth - 20 || p.y < top + 20 || p.y > bottom - 20;
    });
    if (off) fitAll();
  }

  // ---------- resident cache (view only) ------------------------------------
  function cacheWord(word) {
    if (!B.ready || E.renderer.cache[word]) return;
    const r = B.resolve(word);
    if (r) E.renderer.cache[word] = { glyphs: r.glyphs, source: r.source };
  }
  function cacheAll() {
    E.renderer.cache = {};
    Object.values(S.state.manifestations).forEach(m => cacheWord(m.word));
    E.renderer.render();
  }

  // ---------- operations ----------------------------------------------------
  // Placement is a view concern: the host finds a free spot so Presentiations never overlap.
  function freeSpot(x, y) {
    const ms = Object.values(S.state.manifestations), MIN = 82;
    const free = (px, py) => ms.every(m => Math.hypot(m.x - px, m.y - py) >= MIN);
    if (free(x, y)) return { x, y };
    for (let ring = 1; ring <= 8; ring++) {
      const r = ring * 86, steps = 8 + ring * 4;
      for (let i = 0; i < steps; i++) {
        const a = -Math.PI / 2 + (i % 2 ? 1 : -1) * Math.ceil(i / 2) * (2 * Math.PI / steps);
        const px = x + r * Math.cos(a), py = y + r * Math.sin(a);
        if (free(px, py)) return { x: Math.round(px), y: Math.round(py) };
      }
    }
    return { x, y };
  }

  function applyOps(ops, opts) {
    const created = [], userPresent = [];
    for (const raw of ops || []) {
      let op = raw;
      if (op.op === 'PRESENTIATE') {
        const a = { ...(op.args || {}) };
        if (a.x == null || a.y == null) { const c = visibleCenterWorld(); a.x = c.x; a.y = c.y; }
        const spot = freeSpot(Number(a.x), Number(a.y));
        a.x = Math.round(spot.x); a.y = Math.round(spot.y);
        op = { ...op, args: a };
      }
      const e = S.dispatch(op);
      if (e.result === 'applied' && e.op === 'PRESENTIATE') {
        created.push(e.args.manifestationId);
        cacheWord(e.args.word);
        if (e.actor === 'user') userPresent.push(e.args.manifestationId);
      }
      if (e.result === 'rejected' && e.actor === 'echo') {
        IO.emit({ actor: 'system', kind: 'status', text: `ECHO's ${e.op} was not applied: ${e.reason}.` });
      }
    }
    E.renderer.render();
    if (created.length && !(opts && opts.noFit)) ensureVisible(created);
    userPresent.forEach(id => setTimeout(() => echoReact(id), 220));
    return created;
  }

  function handleResult(r) {
    if (!r) return;
    (r.outputs || []).forEach(o => IO.emit(o));
    if (r.overlay) { App.overlay = r.overlay; E.nve.set('overlay', r.overlay); E.renderer.cache = {}; cacheAll(); }
    if (r.mcw) { App.outbox.push(r.mcw); E.nve.set('outbox', App.outbox); }
    applyOps(r.ops);
  }

  function echoReact(manId) {
    if (!B.ready || !S.state.manifestations[manId]) return;
    handleResult(B.onPresentiate(S.snapshot(), manId));
  }

  function send(text, mode) {
    if (!B.ready) {
      toast('ECHO is ' + (B.status === 'error' ? 'offline' : 'still loading'));
      IO.emit({ actor: 'system', kind: 'status', text: `ECHO's runtime is ${B.status}${B.detail ? ' (' + B.detail + ')' : ''}. Your text is still in the box.` });
      return false;
    }
    IO.emit({ actor: 'user', kind: 'text', text: mode === 'TEXT' ? text : `[${mode}] ${text}` });
    handleResult(B.handle(text, mode, S.snapshot()));
    return true;
  }

  function presentiate(word, pos, provenance) {
    word = String(word || '').trim().toLowerCase().replace(/\s+/g, ' ');
    if (!word) return null;
    const c = pos || visibleCenterWorld();
    const id = S.newManId();
    applyOps([{ actor: 'user', op: 'PRESENTIATE', provenance: provenance || 'toolbar', args: {
      manifestationId: id, canonicalId: 'word:' + word, word, renderer: 'circle', x: c.x, y: c.y } }]);
    return id;
  }

  function focusWord(word, provenance) {
    word = String(word || '').toLowerCase();
    const m = Object.values(S.state.manifestations).find(x => x.word === word);
    if (m) {
      S.dispatch({ actor: 'user', op: 'SELECT', provenance: provenance || 'ui', args: { manifestationId: m.id, exclusive: true } });
      centerOn(m);
    } else {
      presentiate(word, null, provenance || 'io-ref');
    }
  }

  function openInspector(manId) {
    const m = S.state.manifestations[manId]; if (!m) return;
    const small = window.innerWidth < 700;
    const p = worldToScreen(m);
    W.dispatch({ op: 'OPEN_WIDGET', spec: { id: 'insp:' + m.word, type: 'INSPECTOR',
      binding: { word: m.word, manId: m.id, canonicalId: m.canonicalId },
      x: small ? 8 : p.x + 44, y: small ? TOOLBAR + 8 : p.y - 60, w: Math.min(320, window.innerWidth - 16), h: 360 } });
  }

  // ---------- canvas pointer interaction -------------------------------------
  const pointers = new Map();
  let drag = null, pinch = null;
  function bindCanvas() {
    const el = svg();
    el.addEventListener('pointerdown', ev => {
      if (ev.button > 0) return;
      pointers.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
      try { el.setPointerCapture(ev.pointerId); } catch (e) { /* ignore */ }
      if (pointers.size === 2) {
        const [a, b] = [...pointers.values()];
        const mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
        pinch = { d0: Math.hypot(a.x - b.x, a.y - b.y) || 1, s0: S.view.scale, world: screenToWorld(mid.x, mid.y) };
        drag = null; E.renderer.render();
        return;
      }
      if (pointers.size > 2) return;
      const g = ev.target.closest && ev.target.closest('.man');
      if (g) {
        const m = S.state.manifestations[g.dataset.id];
        drag = { type: 'man', id: g.dataset.id, pid: ev.pointerId, sx: ev.clientX, sy: ev.clientY, ox: m.x, oy: m.y, moved: false };
      } else {
        drag = { type: 'pan', pid: ev.pointerId, sx: ev.clientX, sy: ev.clientY, vx: S.view.x, vy: S.view.y, moved: false };
      }
    });
    el.addEventListener('pointermove', ev => {
      if (!pointers.has(ev.pointerId)) return;
      pointers.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
      if (pinch && pointers.size >= 2) {
        const [a, b] = [...pointers.values()];
        const d = Math.hypot(a.x - b.x, a.y - b.y) || 1;
        const s = Math.max(0.3, Math.min(3, pinch.s0 * d / pinch.d0));
        const mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }, r = el.getBoundingClientRect();
        S.view.scale = s;
        S.view.x = mid.x - r.left - pinch.world.x * s; S.view.y = mid.y - r.top - pinch.world.y * s;
        E.renderer.render();
        return;
      }
      if (!drag || ev.pointerId !== drag.pid) return;
      const dx = ev.clientX - drag.sx, dy = ev.clientY - drag.sy;
      if (!drag.moved && Math.abs(dx) + Math.abs(dy) > 6) drag.moved = true;
      if (!drag.moved) return;
      if (drag.type === 'man') {
        drag.nx = drag.ox + dx / S.view.scale; drag.ny = drag.oy + dy / S.view.scale;
        E.renderer.render({ [drag.id]: { x: drag.nx, y: drag.ny } });
      } else {
        S.view.x = drag.vx + dx; S.view.y = drag.vy + dy; E.renderer.render();
      }
    });
    const end = ev => {
      const cancelled = ev.type === 'pointercancel';
      pointers.delete(ev.pointerId);
      if (pinch) { if (pointers.size < 2) { pinch = null; scheduleSave(); } drag = null; return; }
      if (!drag || ev.pointerId !== drag.pid) return;
      const d = drag; drag = null;
      if (cancelled) { E.renderer.render(); return; }
      if (d.type === 'man') {
        if (d.moved) {
          S.dispatch({ actor: 'user', op: 'MOVE', target: d.id, args: { x: Math.round(d.nx), y: Math.round(d.ny) },
            provenance: ev.pointerType || 'pointer' });
        } else tapManifestation(d.id, ev);
      } else if (d.moved) {
        scheduleSave();
      } else if (!App.relateMode && S.state.selection.length) {
        S.dispatch({ actor: 'user', op: 'CLEAR_SELECTION', provenance: 'tap-empty' });
      }
    };
    el.addEventListener('pointerup', end);
    el.addEventListener('pointercancel', end);
    el.addEventListener('wheel', ev => {
      ev.preventDefault();
      const r = el.getBoundingClientRect(), w = screenToWorld(ev.clientX, ev.clientY);
      const s = Math.max(0.3, Math.min(3, S.view.scale * (ev.deltaY < 0 ? 1.1 : 1 / 1.1)));
      S.view.scale = s; S.view.x = ev.clientX - r.left - w.x * s; S.view.y = ev.clientY - r.top - w.y * s;
      E.renderer.render(); scheduleSave();
    }, { passive: false });
  }

  function tapManifestation(id, ev) {
    if (App.relateMode) {
      if (!App.relateFirst) {
        App.relateFirst = id; E.renderer.highlight = id; E.renderer.render();
        toast('Now tap the second Presentiation');
      } else if (App.relateFirst === id) {
        toast('Tap a different Presentiation');
      } else {
        const e = S.dispatch({ actor: 'user', op: 'RELATE', provenance: 'relate-mode',
          args: { from: App.relateFirst, to: id, type: 'is-a', label: 'is-a' } });
        if (e.result === 'rejected') toast(e.reason);
        setRelate(false);
      }
      return;
    }
    const sel = S.state.selection;
    if (!App.multi && !ev.shiftKey && sel.length === 1 && sel[0] === id) { openInspector(id); return; }
    S.dispatch({ actor: 'user', op: 'SELECT', provenance: ev.pointerType || 'pointer',
      args: { manifestationId: id, exclusive: !(App.multi || ev.shiftKey) } });
  }

  function setRelate(on) {
    App.relateMode = on; App.relateFirst = null; E.renderer.highlight = null;
    $('#btn-relate').classList.toggle('on', on);
    $('#btn-relate').setAttribute('aria-pressed', String(on));
    E.renderer.render();
    if (on) toast('Relate: tap the first Presentiation');
  }

  // ---------- toolbar, dialog, menu -------------------------------------------
  function bindChrome() {
    const dlg = $('#present-dialog'), inp = $('#present-input');
    const openDlg = () => { dlg.hidden = false; $('#backdrop').hidden = false; inp.value = ''; inp.focus(); };
    const closeDlg = () => { dlg.hidden = true; $('#backdrop').hidden = true; inp.blur(); };
    $('#btn-present').addEventListener('click', openDlg);
    $('#present-cancel').addEventListener('click', closeDlg);
    $('#backdrop').addEventListener('click', () => { closeDlg(); closeMenu(); });
    $('#present-form').addEventListener('submit', ev => {
      ev.preventDefault();
      const word = inp.value.trim();
      if (!word) { inp.focus(); return; }
      closeDlg();
      const id = presentiate(word, null, 'toolbar');
      if (id) S.dispatch({ actor: 'user', op: 'SELECT', provenance: 'toolbar', args: { manifestationId: id, exclusive: true } });
    });

    $('#btn-relate').addEventListener('click', () => setRelate(!App.relateMode));
    $('#btn-multi').addEventListener('click', () => {
      App.multi = !App.multi;
      $('#btn-multi').classList.toggle('on', App.multi);
      $('#btn-multi').setAttribute('aria-pressed', String(App.multi));
      toast(App.multi ? 'Multi-select on: taps add to the selection' : 'Multi-select off');
    });
    $('#btn-clear').addEventListener('click', () => {
      if (App.relateMode) setRelate(false);
      if (S.state.selection.length) S.dispatch({ actor: 'user', op: 'CLEAR_SELECTION', provenance: 'toolbar' });
      else toast('Nothing selected');
    });
    $('#rt-pill').addEventListener('click', () => openWidget('STATUS'));

    const menu = $('#menu');
    $('#btn-menu').addEventListener('click', () => { menu.hidden ? openMenu() : closeMenu(); });
    function openMenu() { menu.hidden = false; $('#btn-menu').setAttribute('aria-expanded', 'true'); }
    function closeMenu() { menu.hidden = true; $('#btn-menu').setAttribute('aria-expanded', 'false'); }
    document.addEventListener('pointerdown', ev => {
      if (!menu.hidden && !menu.contains(ev.target) && !ev.target.closest('#btn-menu')) closeMenu();
    });
    menu.addEventListener('click', ev => {
      const b = ev.target.closest('button[data-cmd]'); if (!b) return;
      closeMenu();
      const c = b.dataset.cmd;
      if (c === 'inspect') {
        const s = S.state.selection;
        if (!s.length) toast('Select a Presentiation first'); else s.forEach(openInspector);
      } else if (c === 'query-sel') {
        openWidget('IO_DOCK'); send('selection', 'QUERY');
      } else if (c === 'fit') fitAll();
      else if (c === 'lattice' || c === 'circle') {
        const ids = S.state.selection.length ? S.state.selection : Object.keys(S.state.manifestations);
        ids.forEach(id => S.dispatch({ actor: 'user', op: 'SET_RENDERER', target: id, provenance: 'menu', args: { renderer: c } }));
      } else if (c === 'save-layout') saveLayout();
      else if (c === 'restore-layout') restoreLayout();
      else openWidget(c);
    });
    document.addEventListener('keydown', ev => {
      if (ev.key !== 'Escape') return;
      if (!dlg.hidden) closeDlg();
      else if (!menu.hidden) closeMenu();
      else if (App.relateMode) setRelate(false);
    });
  }

  function openWidget(type) {
    const small = window.innerWidth < 700;
    const specs = {
      IO_DOCK: { id: 'io', type: 'IO_DOCK', docked: small, x: window.innerWidth - 392, y: TOOLBAR + 12, w: 380, h: window.innerHeight - TOOLBAR - 24 },
      AUDIT: { id: 'audit', type: 'AUDIT', x: 8, y: TOOLBAR + 8, w: 340, h: 340 },
      STATUS: { id: 'status', type: 'STATUS', x: 8, y: TOOLBAR + 8, w: 330, h: 380 },
      REGISTRY: { id: 'registry', type: 'REGISTRY', x: 8, y: TOOLBAR + 8, w: 300, h: 380 },
      DATA: { id: 'data', type: 'DATA', x: 8, y: TOOLBAR + 8, w: 330, h: 420 },
    };
    const spec = specs[type]; if (!spec) return;
    W.dispatch({ op: 'OPEN_WIDGET', spec });
  }

  // ---------- runtime -------------------------------------------------------
  function paintStatus() {
    const pill = $('#rt-pill');
    pill.dataset.state = B.status;
    $('#rt-text').textContent = B.status === 'ready' ? 'ECHO ready' : B.status === 'error' ? 'ECHO offline' :
      B.status === 'loading' ? 'Loading\u2026' : 'ECHO';
    pill.title = B.detail || B.status;
    if (W.items.has('status')) W.refresh('status');
  }
  async function bootRuntime() {
    const r = await B.start({ instance_id: App.instanceId, overlay: App.overlay });
    if (!r) {
      IO.emit({ actor: 'system', kind: 'error', text: `ECHO's runtime did not load: ${B.error}. The Canvas still works; ECHO's reactions return when the runtime loads. Open the status pill to retry.` });
      return;
    }
    if (!App.instanceId) { App.instanceId = r.instance_id; E.nve.set('instance', App.instanceId); }
    cacheAll();
    const dl = $('#resident-list');
    dl.innerHTML = (B.words() || []).map(w => `<option value="${E.renderer.esc(w.word)}"></option>`).join('');
    if (W.items.has('registry')) W.refresh('registry');
    IO.emit({ actor: 'echo', kind: 'status', text: `\u05e8 ECHO online \u00b7 kernel ${r.identity['kernel lines']} lines \u00b7 ${r.identity['canonical residents']} residents` +
      (r.identity['overlay residents'] ? ` \u00b7 ${r.identity['overlay residents']} local` : '') + '. Type help for commands.' });
  }

  async function flushOutbox() {
    if (!App.outbox.length) { toast('Outbox is empty'); return; }
    if (!App.settings.endpoint) { toast('Set a gateway endpoint first'); return; }
    let sent = 0;
    const keep = [];
    for (const env of App.outbox) {
      try {
        const res = await fetch(App.settings.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(env) });
        if (res.ok) sent++; else keep.push(env);
      } catch (e) { keep.push(env); }
    }
    App.outbox = keep; E.nve.set('outbox', keep);
    IO.emit({ actor: 'system', kind: keep.length ? 'error' : 'status', text: `MCW: ${sent} sent, ${keep.length} still queued.` });
  }

  function exportJSON() {
    const data = { format: 'echo-notebook/0.1', exported: new Date().toISOString(), instance: App.instanceId,
      canvas: { state: S.state, log: S.log, view: S.view }, layout: W.serialize(), overlay: App.overlay,
      io: IO.history.slice(-150), outbox: App.outbox };
    const blob = new Blob([JSON.stringify(data, null, 1)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'echo-notebook-' + new Date().toISOString().slice(0, 10) + '.json';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    toast('Notebook exported');
  }
  function importJSON() {
    const inp = document.createElement('input');
    inp.type = 'file'; inp.accept = 'application/json,.json';
    inp.addEventListener('change', () => {
      const f = inp.files && inp.files[0]; if (!f) return;
      f.text().then(txt => {
        const d = JSON.parse(txt);
        if (!d.canvas || !d.canvas.state) throw new Error('not an ECHO notebook file');
        S.load(d.canvas);
        App.overlay = d.overlay || {}; E.nve.set('overlay', App.overlay);
        if (B.ready) B.setOverlay(App.overlay);
        if (Array.isArray(d.outbox)) { App.outbox = d.outbox; E.nve.set('outbox', App.outbox); }
        if (Array.isArray(d.layout)) W.restore(d.layout);
        cacheAll(); fitAll();
        IO.emit({ actor: 'system', kind: 'status', text: `Imported ${Object.keys(S.state.manifestations).length} Presentiations and ${S.log.length} operations.` });
      }).catch(e => toast('Import failed: ' + e.message));
    });
    inp.click();
  }
  async function wipe() {
    if (!confirm('Clear this device\u2019s notebook (Canvas, layout, overlay, history, outbox)? Export first if you want a copy.')) return;
    await E.nve.clear();
    location.reload();
  }

  let toastT = null;
  function toast(msg) {
    const t = $('#toast'); t.textContent = msg; t.hidden = false;
    clearTimeout(toastT); toastT = setTimeout(() => { t.hidden = true; }, 2200);
  }

  // ---------- init ------------------------------------------------------------
  async function init() {
    bindCanvas(); bindChrome();
    S.subscribe(e => { E.renderer.render(); scheduleSave(); E.audit.refresh(); if (e.op === 'SELECT' || e.op === 'CLEAR_SELECTION') paintSel(); });
    W.onChange = autosaveLayout;
    B.events.addEventListener('status', paintStatus);

    const [canvas, layout, io, overlay, outbox, settings, instance] = await Promise.all(
      ['canvas', 'layout:auto', 'io', 'overlay', 'outbox', 'settings', 'instance'].map(k => E.nve.get(k)));
    if (canvas) S.load(canvas);
    if (Array.isArray(io)) IO.history = io;
    App.overlay = overlay || {}; App.outbox = outbox || []; App.settings = settings || { endpoint: '' };
    App.instanceId = instance || null;
    E.renderer.render();

    if (Array.isArray(layout) && layout.length) W.restore(layout);
    else openWidget('IO_DOCK');

    if (!IO.history.length) {
      IO.emit({ actor: 'system', kind: 'status', text:
        'Tap + to Presentiate a word. ECHO identifies it and places its hypernym above it. Tap a circle to select it; tap it again to open its Inspector. Drag circles to move them, drag empty space to pan, pinch to zoom.' });
    }
    paintStatus(); paintSel();
    bootRuntime();

    if ('serviceWorker' in navigator && (location.protocol === 'https:' || ['localhost', '127.0.0.1'].includes(location.hostname))) {
      navigator.serviceWorker.register('./sw.js').catch(e => console.warn('SW', e));
    }
  }
  function paintSel() {
    const n = S.state.selection.length;
    $('#sel-count').textContent = n ? String(n) : '';
    $('#sel-count').hidden = !n;
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})(window.ECHO = window.ECHO || {});
