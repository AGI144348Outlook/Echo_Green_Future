/* Widget types beyond the I/O dock: Inspector, Audit, ECHO status, Registry, MCW & data. */
(function (E) {
  'use strict';
  const esc = t => E.renderer.esc(t);
  const W = E.widgets;

  // ---- Audit: canvas operations + workspace (widget) operations ----------
  const A = E.audit = { ws: [], filter: 'all', workspace, refresh };
  function workspace(entry) {
    A.ws.push({ ...entry, scope: 'workspace', ts: Date.now() });
    if (A.ws.length > 1000) A.ws.splice(0, A.ws.length - 1000);
    refresh();
  }
  let pending = false;
  function refresh() {
    if (pending) return; pending = true;
    requestAnimationFrame(() => {
      pending = false;
      const list = document.querySelector('.audit-list');
      if (!list) return;
      const all = E.store.log.map(o => ({ ...o, scope: 'canvas' })).concat(A.ws)
        .filter(o => A.filter === 'all' || o.actor === A.filter)
        .sort((a, b) => b.ts - a.ts).slice(0, 150);
      list.innerHTML = all.length ? all.map(o => {
        const what = o.args && o.args.word ? ' ' + o.args.word : (o.id && o.scope === 'workspace' ? ' ' + o.id : '');
        const tgt = o.target ? ' \u2192 ' + o.target : '';
        return `<div class="a-row ${o.actor} ${o.result}"><span class="a-op">${esc(o.op)}${esc(what)}${esc(tgt)}</span>` +
          `<span class="a-meta">${esc(o.actor)} \u00b7 ${esc(o.scope)}${o.provenance ? ' \u00b7 ' + esc(o.provenance) : ''}` +
          `${o.result === 'rejected' ? ' \u00b7 rejected: ' + esc(o.reason || '') : ''} \u00b7 ${new Date(o.ts).toLocaleTimeString()}</span></div>`;
      }).join('') : '<p class="muted pad">No operations yet.</p>';
    });
  }
  W.register('AUDIT', {
    title: 'Operation audit', icon: '\u25ce',
    build(body) {
      body.innerHTML = `<div class="bar">` + ['all', 'user', 'echo'].map(f => `<button class="seg ${A.filter === f ? 'on' : ''}" data-f="${f}">${f}</button>`).join('') +
        `<button class="replay">Replay check</button></div><div class="audit-list"></div>`;
      body.querySelectorAll('.seg').forEach(b => b.addEventListener('click', () => {
        A.filter = b.dataset.f; body.querySelectorAll('.seg').forEach(x => x.classList.toggle('on', x === b)); refresh();
      }));
      body.querySelector('.replay').addEventListener('click', () => {
        const rebuilt = E.store.replay(E.store.log);
        const strip = s => JSON.stringify({ m: s.manifestations, r: s.relations });
        const ok = strip(rebuilt) === strip(E.store.state);
        const n = E.store.log.filter(o => o.result === 'applied').length;
        E.io.emit({ actor: 'system', kind: ok ? 'status' : 'error',
          text: ok ? `Replay of ${n} applied operations reproduces the current Canvas exactly.`
                   : `Replay of ${n} operations does not match the current Canvas (the log may have been trimmed).` });
        E.app.toast(ok ? 'Replay matches' : 'Replay differs');
      });
      refresh();
    },
  });

  // ---- Inspector: bound to a semantic resident (and optionally a Presentiation)
  W.register('INSPECTOR', {
    title: 'Inspector', icon: '\u25c8',
    titleFor: w => 'Inspector: ' + ((w.binding && w.binding.word) || ''),
    build(body, w) {
      const word = (w.binding && w.binding.word) || '';
      const r = E.bridge.ready ? E.bridge.resolve(word) : null;
      E.store.dispatch({ actor: 'user', op: 'RESOLVE', args: { word }, provenance: 'inspector' });
      const man = w.binding && E.store.state.manifestations[w.binding.manId];
      const count = Object.values(E.store.state.manifestations).filter(m => m.word === word).length;
      const row = (k, v) => `<div class="kv"><span>${esc(k)}</span><span>${v}</span></div>`;
      const links = arr => (arr && arr.length) ? arr.map(x => `<button class="chip" data-word="${esc(x)}">${esc(x)}</button>`).join('') : '\u2014';
      body.innerHTML = r ? (
        `<div class="insp-glyph">${esc(r.glyphs || '?')}</div>` +
        row('word', esc(r.word)) + row('canonical id', `<code>${esc(r.id)}</code>`) +
        row('source', esc(r.source)) + row('definition', esc(r.def)) +
        row('LHEA', esc(r.lhea || '\u2014')) + row('gematria', esc(r.gematria)) +
        row('hypernyms', links(r.hypernyms)) + row('hyponyms', links(r.hyponyms)) +
        row('on Canvas', `${count} Presentiation${count === 1 ? '' : 's'}`)
      ) : `<p class="muted pad">ECHO's runtime is ${esc(E.bridge.status)}. Identity: <code>word:${esc(word)}</code></p>`;
      body.insertAdjacentHTML('beforeend',
        `<div class="bar wrap">` +
        `<button data-a="again">Presentiate again</button>` +
        (man ? `<button data-a="render">Draw as ${man.renderer === 'lattice' ? 'circle' : 'lattice'}</button>` : '') +
        (r && r.chain && r.chain.length ? `<button data-a="chain">Show chain</button>` : '') +
        `</div>`);
      body.addEventListener('click', (ev) => {
        const chip = ev.target.closest('.chip');
        if (chip) { E.app.focusWord(chip.dataset.word, 'inspector'); return; }
        const b = ev.target.closest('button[data-a]'); if (!b) return;
        if (b.dataset.a === 'again') {
          const base = man || Object.values(E.store.state.manifestations).find(m => m.word === word);
          E.app.presentiate(word, base ? { x: base.x + 120, y: base.y + 30 } : null, 'inspector');
          W.dispatch({ op: 'BIND_WIDGET', id: w.id, binding: w.binding });
        }
        if (b.dataset.a === 'render' && man) {
          E.store.dispatch({ actor: 'user', op: 'SET_RENDERER', target: man.id,
            args: { renderer: man.renderer === 'lattice' ? 'circle' : 'lattice' }, provenance: 'inspector' });
          W.dispatch({ op: 'BIND_WIDGET', id: w.id, binding: w.binding });
        }
        if (b.dataset.a === 'chain') E.app.send('chain ' + word, 'CANVAS');
      });
    },
  });

  // ---- ECHO status -----------------------------------------------------
  W.register('STATUS', {
    title: 'ECHO runtime', icon: '\u05e8',
    build(body) {
      const B = E.bridge;
      const id = B.identity;
      body.innerHTML =
        `<div class="kv"><span>status</span><span class="st-${esc(B.status)}">${esc(B.status)}${B.detail ? ' \u00b7 ' + esc(B.detail) : ''}</span></div>` +
        (id ? Object.entries(id).map(([k, v]) => `<div class="kv"><span>${esc(k)}</span><span>${esc(v)}</span></div>`).join('') : '') +
        (B.error ? `<p class="err pad">${esc(B.error)}</p><p class="muted pad">Pyodide needs a network connection the first time, and the app must be served over http(s), not opened as a file.</p>` : '') +
        `<div class="bar wrap"><button data-a="cycle" ${B.ready ? '' : 'disabled'}>Run Governor cycle</button>` +
        `<button data-a="identify" ${B.ready ? '' : 'disabled'}>Identify</button>` +
        (B.status === 'error' ? `<button data-a="retry">Retry loading</button>` : '') + `</div>`;
      body.querySelectorAll('button[data-a]').forEach(b => b.addEventListener('click', () => {
        if (b.dataset.a === 'cycle') E.app.send('cycle', 'QUERY');
        if (b.dataset.a === 'identify') E.app.send('identify', 'QUERY');
        if (b.dataset.a === 'retry') E.app.bootRuntime();
      }));
    },
  });

  // ---- Registry browser ----------------------------------------------------
  W.register('REGISTRY', {
    title: 'Registry', icon: '\u2261',
    build(body) {
      if (!E.bridge.ready) { body.innerHTML = `<p class="muted pad">Available once ECHO's runtime is ready (${esc(E.bridge.status)}).</p>`; return; }
      const all = E.bridge.words() || [];
      body.innerHTML = `<div class="bar"><input type="search" placeholder="Filter ${all.length} residents" aria-label="Filter residents"></div><div class="reg-list"></div>`;
      const list = body.querySelector('.reg-list'), q = body.querySelector('input');
      const draw = () => {
        const f = q.value.trim().toLowerCase();
        list.innerHTML = all.filter(r => !f || r.word.includes(f)).map(r =>
          `<button class="reg-row" data-word="${esc(r.word)}"><span class="g">${esc(r.glyphs)}</span><span class="w">${esc(r.word)}</span>` +
          `<span class="s ${esc(r.source)}">${r.source === 'canonical' ? '' : esc(r.source)}</span></button>`).join('') || '<p class="muted pad">No match.</p>';
      };
      q.addEventListener('input', draw);
      list.addEventListener('click', ev => { const b = ev.target.closest('.reg-row'); if (b) E.app.focusWord(b.dataset.word, 'registry'); });
      draw();
    },
  });

  // ---- MCW & data ----------------------------------------------------------
  W.register('DATA', {
    title: 'MCW & data', icon: '\u21c5',
    build(body) {
      const s = E.app.settings;
      body.innerHTML =
        `<div class="pad"><label class="lbl" for="mcw-ep">MCW gateway endpoint</label>` +
        `<input id="mcw-ep" type="url" inputmode="url" placeholder="https://your-worker.workers.dev/mcw" value="${esc(s.endpoint || '')}">` +
        `<p class="muted small">No keys are stored in this app. Authentication belongs to the gateway.</p>` +
        `<div class="bar wrap"><button data-a="save-ep">Save endpoint</button><button data-a="send">Send outbox (${E.app.outbox.length})</button></div>` +
        `<hr><div class="bar wrap"><button data-a="export">Export notebook JSON</button><button data-a="import">Import JSON</button></div>` +
        `<div class="bar wrap"><button data-a="save-layout">Save layout</button><button data-a="restore-layout">Restore layout</button></div>` +
        `<hr><div class="bar wrap"><button data-a="wipe" class="danger">Clear local notebook</button></div>` +
        `<p class="muted small">Instance: <code>${esc(E.app.instanceId || '\u2014')}</code></p></div>`;
      body.querySelectorAll('button[data-a]').forEach(b => b.addEventListener('click', () => {
        const a = b.dataset.a;
        if (a === 'save-ep') { E.app.settings.endpoint = body.querySelector('#mcw-ep').value.trim(); E.app.saveSettings(); E.app.toast('Endpoint saved'); }
        if (a === 'send') E.app.flushOutbox().then(() => W.dispatch({ op: 'BIND_WIDGET', id: 'data', binding: null }));
        if (a === 'export') E.app.exportJSON();
        if (a === 'import') E.app.importJSON();
        if (a === 'save-layout') E.app.saveLayout();
        if (a === 'restore-layout') E.app.restoreLayout();
        if (a === 'wipe') E.app.wipe();
      }));
    },
  });
})(window.ECHO = window.ECHO || {});
