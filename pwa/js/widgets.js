/* Notebook Widgets. Widget identity is separate from semantic resident identity
   and from Canvas Presentiation identity. A widget may be BOUND to a resident or
   a Presentiation; closing or moving it never touches what it is bound to.
   Layouts are workspace state (local NVE), not Registry semantics. */
(function (E) {
  'use strict';
  const TOOLBAR = 48;
  const W = E.widgets = {
    types: {},            // type -> { title, icon, build(body, w) }
    items: new Map(),     // id -> widget model
    z: 100,
    register(type, def) { this.types[type] = def; },
    dispatch, open, close, focus, serialize, restore, clampAll,
    refresh(id) { const w = this.items.get(id); if (w) rebuild(w); },
    onChange: null,
  };

  function vw() { return window.innerWidth; }
  function vh() { return window.innerHeight; }

  // Widget API: OPEN_WIDGET CLOSE_WIDGET FOCUS_WIDGET MOVE_WIDGET RESIZE_WIDGET
  // DOCK_WIDGET MINIMIZE_WIDGET MAXIMIZE_WIDGET BIND_WIDGET SAVE_LAYOUT RESTORE_LAYOUT
  function dispatch(op) {
    const actor = op.actor || 'user';
    const w = op.id && W.items.get(op.id);
    // ECHO may open and focus widgets, but may not rearrange or close the person's workspace.
    if (actor === 'echo' && w && w.owner === 'user' &&
        ['CLOSE_WIDGET', 'MOVE_WIDGET', 'RESIZE_WIDGET', 'DOCK_WIDGET', 'MAXIMIZE_WIDGET', 'MINIMIZE_WIDGET'].includes(op.op)) {
      E.audit && E.audit.workspace({ ...op, actor, result: 'rejected', reason: 'user-owned widget' });
      return false;
    }
    switch (op.op) {
      case 'OPEN_WIDGET': open(op.spec, actor); break;
      case 'CLOSE_WIDGET': close(op.id); break;
      case 'FOCUS_WIDGET': focus(op.id); break;
      case 'MOVE_WIDGET': if (w) { w.x = op.x; w.y = op.y; place(w); } break;
      case 'RESIZE_WIDGET': if (w) { w.w = op.w; w.h = op.h; place(w); } break;
      case 'DOCK_WIDGET': if (w) { w.docked = !w.docked; w.maximized = false; place(w); } break;
      case 'MINIMIZE_WIDGET': if (w) { w.minimized = !w.minimized; place(w); } break;
      case 'MAXIMIZE_WIDGET': if (w) { w.maximized = !w.maximized; w.minimized = false; place(w); } break;
      case 'BIND_WIDGET': if (w) { w.binding = op.binding; rebuild(w); } break;
      default: return false;
    }
    if (!['FOCUS_WIDGET'].includes(op.op)) E.audit && E.audit.workspace({ ...op, spec: undefined, actor, result: 'applied' });
    if (W.onChange) W.onChange(op);
    return true;
  }

  function open(spec, actor) {
    const id = spec.id || (spec.type + ':' + Date.now().toString(36));
    const existing = W.items.get(id);
    if (existing) {
      if (spec.binding) { existing.binding = spec.binding; rebuild(existing); }
      existing.minimized = false; place(existing); focus(id);
      return existing;
    }
    const def = W.types[spec.type];
    if (!def) return null;
    const w = {
      id, type: spec.type, title: spec.title || def.title, icon: def.icon || '\u25a1',
      x: spec.x != null ? spec.x : 12, y: spec.y != null ? spec.y : TOOLBAR + 12,
      w: spec.w || Math.min(340, vw() - 24), h: spec.h || 320,
      minimized: !!spec.minimized, maximized: !!spec.maximized, docked: !!spec.docked,
      binding: spec.binding || null, owner: spec.owner || actor || 'user', el: null,
    };
    // Cascade so a new widget never sits exactly on top of another one.
    for (let i = 0; i < 12 && [...W.items.values()].some(o => !o.docked && !o.maximized && Math.abs(o.x - w.x) < 6 && Math.abs(o.y - w.y) < 6); i++) {
      w.x += 22; w.y += 26;
    }
    W.items.set(id, w);
    build(w);
    focus(id);
    return w;
  }

  function build(w) {
    const el = document.createElement('section');
    el.className = 'widget';
    el.dataset.id = w.id;
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-label', w.title);
    el.innerHTML =
      `<header class="w-head"><span class="w-icon" aria-hidden="true">${w.icon}</span>` +
      `<span class="w-title"></span>` +
      `<button class="w-btn" data-act="dock" title="Dock to bottom / float" aria-label="Dock or float">\u2913</button>` +
      `<button class="w-btn" data-act="min" title="Collapse" aria-label="Collapse or expand">\u2212</button>` +
      `<button class="w-btn" data-act="max" title="Maximize" aria-label="Maximize or restore">\u25a1</button>` +
      `<button class="w-btn" data-act="close" title="Close" aria-label="Close">\u2715</button></header>` +
      `<div class="w-body"></div><div class="w-resize" aria-hidden="true"></div>`;
    el.querySelector('.w-title').textContent = w.title;
    w.el = el;
    document.getElementById('widget-layer').appendChild(el);

    el.addEventListener('pointerdown', () => focus(w.id), true);
    el.querySelectorAll('.w-btn').forEach(b => b.addEventListener('click', (ev) => {
      ev.stopPropagation();
      const act = b.dataset.act;
      if (act === 'close') dispatch({ op: 'CLOSE_WIDGET', id: w.id });
      if (act === 'min') dispatch({ op: 'MINIMIZE_WIDGET', id: w.id });
      if (act === 'max') dispatch({ op: 'MAXIMIZE_WIDGET', id: w.id });
      if (act === 'dock') dispatch({ op: 'DOCK_WIDGET', id: w.id });
    }));

    // Drag by header
    const head = el.querySelector('.w-head');
    let drag = null;
    head.addEventListener('pointerdown', (ev) => {
      if (ev.target.closest('.w-btn') || w.maximized || w.docked) return;
      drag = { px: ev.clientX, py: ev.clientY, x: w.x, y: w.y, moved: false };
      head.setPointerCapture(ev.pointerId);
    });
    head.addEventListener('pointermove', (ev) => {
      if (!drag) return;
      const dx = ev.clientX - drag.px, dy = ev.clientY - drag.py;
      if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true;
      w.x = drag.x + dx; w.y = drag.y + dy; place(w);
    });
    const endDrag = () => {
      if (drag && drag.moved) dispatch({ op: 'MOVE_WIDGET', id: w.id, x: w.x, y: w.y });
      drag = null;
    };
    head.addEventListener('pointerup', endDrag);
    head.addEventListener('pointercancel', endDrag);
    head.addEventListener('dblclick', () => dispatch({ op: 'MAXIMIZE_WIDGET', id: w.id }));

    // Resize from corner
    const grip = el.querySelector('.w-resize');
    let rs = null;
    grip.addEventListener('pointerdown', (ev) => {
      if (w.maximized || w.minimized) return;
      ev.stopPropagation();
      rs = { px: ev.clientX, py: ev.clientY, w: w.w, h: w.h };
      grip.setPointerCapture(ev.pointerId);
    });
    grip.addEventListener('pointermove', (ev) => {
      if (!rs) return;
      w.w = Math.max(220, rs.w + ev.clientX - rs.px);
      w.h = Math.max(140, rs.h + ev.clientY - rs.py);
      place(w);
    });
    const endRs = () => { if (rs) dispatch({ op: 'RESIZE_WIDGET', id: w.id, w: w.w, h: w.h }); rs = null; };
    grip.addEventListener('pointerup', endRs);
    grip.addEventListener('pointercancel', endRs);

    rebuild(w);
    place(w);
  }

  function rebuild(w) {
    const def = W.types[w.type];
    // Fresh body element each time so listeners from a previous build never stack.
    const old = w.el.querySelector('.w-body');
    const body = document.createElement('div');
    body.className = 'w-body';
    old.replaceWith(body);
    if (def && def.build) def.build(body, w);
    if (def && def.titleFor) { w.title = def.titleFor(w); w.el.querySelector('.w-title').textContent = w.title; }
  }

  function place(w) {
    const el = w.el; if (!el) return;
    el.classList.toggle('minimized', w.minimized);
    el.classList.toggle('maximized', w.maximized);
    el.classList.toggle('docked', w.docked && !w.maximized);
    if (w.maximized || w.docked) {
      el.style.left = el.style.top = el.style.width = el.style.height = '';
      return;
    }
    w.w = Math.min(w.w, vw() - 8);
    w.h = Math.min(w.h, vh() - TOOLBAR - 8);
    w.x = Math.min(Math.max(0, w.x), Math.max(0, vw() - 80));
    w.y = Math.min(Math.max(TOOLBAR, w.y), Math.max(TOOLBAR, vh() - 44));
    el.style.left = w.x + 'px';
    el.style.top = w.y + 'px';
    el.style.width = w.w + 'px';
    el.style.height = w.minimized ? '' : w.h + 'px';
  }

  function focus(id) {
    const w = W.items.get(id); if (!w) return;
    w.el.style.zIndex = ++W.z;
    W.items.forEach(o => o.el && o.el.classList.toggle('focused', o === w));
  }

  function close(id) {
    const w = W.items.get(id); if (!w) return;
    const def = W.types[w.type];
    if (def && def.onClose) def.onClose(w);
    w.el.remove();
    W.items.delete(id);
  }

  function serialize() {
    return [...W.items.values()].sort((a, b) => (+a.el.style.zIndex) - (+b.el.style.zIndex)).map(w => ({
      id: w.id, type: w.type, x: w.x, y: w.y, w: w.w, h: w.h, minimized: w.minimized,
      maximized: w.maximized, docked: w.docked, binding: w.binding, owner: w.owner }));
  }

  function restore(list) {
    if (!Array.isArray(list)) return;
    [...W.items.keys()].forEach(close);
    for (const s of list) if (W.types[s.type]) open(s, s.owner || 'user');
  }

  function clampAll() { W.items.forEach(place); }
  window.addEventListener('resize', clampAll);
})(window.ECHO = window.ECHO || {});
