/* Renderer: draws CanvasState. Geometry only; identity lives in canonicalId.
   Changing how something is drawn never changes what it is. */
(function (E) {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const R = E.renderer = { render, cache: {}, highlight: null };

  function esc(t) {
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function short(w) { return w.length > 11 ? w.slice(0, 10) + '\u2026' : w; }

  function render(overrides) {
    const st = E.store.state, v = E.store.view;
    const world = document.getElementById('world');
    world.setAttribute('transform', `translate(${v.x},${v.y}) scale(${v.scale})`);
    const pos = id => (overrides && overrides[id]) || st.manifestations[id];

    let rels = '';
    for (const r of Object.values(st.relations)) {
      const a = pos(r.from), b = pos(r.to);
      if (!a || !b) continue;
      const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy) || 1;
      const pad = 36, ux = dx / len, uy = dy / len;
      const x1 = a.x + ux * pad, y1 = a.y + uy * pad, x2 = b.x - ux * (pad + 4), y2 = b.y - uy * (pad + 4);
      rels += `<line class="rel ${r.actor === 'echo' ? 'rel-echo' : ''}" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" marker-end="url(#arrow)"/>` +
        `<text class="rel-label" x="${(a.x + b.x) / 2}" y="${(a.y + b.y) / 2 - 5}">${esc(r.label)}</text>`;
    }
    document.getElementById('rels').innerHTML = rels;

    const sel = new Set(st.selection);
    let out = '';
    for (const m of Object.values(st.manifestations)) {
      const p = pos(m.id);
      const info = R.cache[m.word] || {};
      const cls = ['man', m.actor === 'echo' ? 'by-echo' : 'by-user',
        sel.has(m.id) ? 'selected' : '', info.source === 'gap' ? 'gap' : '',
        info.source === 'local-overlay' ? 'overlay' : '', R.highlight === m.id ? 'pending' : ''].join(' ');
      const glyph = esc((info.glyphs || '').slice(0, 4));
      const title = `<title>${esc(m.word)} \u00b7 ${esc(m.canonicalId)}${info.source ? ' \u00b7 ' + info.source : ''}</title>`;
      if (m.renderer === 'lattice') {
        out += `<g class="${cls} lattice" data-id="${esc(m.id)}" transform="translate(${p.x},${p.y})">${title}` +
          `<rect class="halo" x="-38" y="-38" width="76" height="76" rx="10"/>` +
          `<rect class="body" x="-30" y="-30" width="60" height="60" rx="6"/>` +
          `<text class="glyph big" y="4">${glyph || '?'}</text>` +
          `<text class="word small" y="22">${esc(short(m.word))}</text></g>`;
      } else {
        out += `<g class="${cls}" data-id="${esc(m.id)}" transform="translate(${p.x},${p.y})">${title}` +
          `<circle class="halo" r="38"/><circle class="body" r="30"/>` +
          `<text class="word" y="3">${esc(short(m.word))}</text>` +
          `<text class="glyph" y="18">${glyph}</text></g>`;
      }
    }
    document.getElementById('mans').innerHTML = out;
    const empty = document.getElementById('empty-hint');
    if (empty) empty.hidden = Object.keys(st.manifestations).length > 0;
  }
  R.esc = esc;
})(window.ECHO = window.ECHO || {});
