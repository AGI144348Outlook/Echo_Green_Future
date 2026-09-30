/* Notebook I/O dock: an interface into the NotebookBus, not a chat widget.
   Input: TEXT, QUERY or CANVAS COMMAND. Output: text, status, errors, matrices,
   plus whatever Canvas operations the runtime returns (applied by app.js). */
(function (E) {
  'use strict';
  const esc = t => E.renderer.esc(t);
  const IO = E.io = { history: [], mode: 'TEXT', emit, outEl: null, inputEl: null, clearHistory };
  const coarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;

  function entryHTML(e) {
    const who = e.actor === 'user' ? 'You' : (e.actor === 'echo' ? '\u05e8 ECHO' : 'Notebook');
    let body = '';
    if (e.kind === 'matrix' && Array.isArray(e.rows)) {
      const head = (e.columns || []).map(c => `<th>${esc(c)}</th>`).join('');
      const rows = e.rows.map(r => '<tr>' + r.map(c => `<td>${esc(c)}</td>`).join('') + '</tr>').join('');
      body = `<div class="io-mtitle">${esc(e.text || '')}</div><div class="io-table"><table>${head ? '<thead><tr>' + head + '</tr></thead>' : ''}<tbody>${rows}</tbody></table></div>` +
        (e.note ? `<div class="io-note">${esc(e.note)}</div>` : '');
    } else {
      body = `<div class="io-text">${esc(e.text || '')}</div>`;
    }
    const refs = [...new Set(e.refs || [])].filter(Boolean);
    const chips = refs.length ? `<div class="chips">${refs.map(r => `<button class="chip" data-word="${esc(r)}">${esc(r)}</button>`).join('')}</div>` : '';
    return `<div class="io-entry ${e.actor} k-${e.kind || 'text'}"><div class="io-who">${who}</div>${body}${chips}</div>`;
  }

  function emit(e) {
    e.ts = e.ts || Date.now();
    IO.history.push(e);
    if (IO.history.length > 300) IO.history.splice(0, IO.history.length - 300);
    if (IO.outEl && IO.outEl.isConnected) {
      IO.outEl.insertAdjacentHTML('beforeend', entryHTML(e));
      IO.outEl.scrollTop = IO.outEl.scrollHeight;
    }
    E.app && E.app.persistIO();
  }

  function clearHistory() { IO.history = []; if (IO.outEl) IO.outEl.innerHTML = ''; E.app && E.app.persistIO(); }

  E.widgets.register('IO_DOCK', {
    title: 'Notebook I/O', icon: '\u2328',
    build(body) {
      body.classList.add('io');
      body.innerHTML =
        `<div class="io-modes" role="tablist">` +
        ['TEXT', 'QUERY', 'CANVAS'].map(m => `<button role="tab" class="mode ${IO.mode === m ? 'on' : ''}" data-mode="${m}">${m === 'CANVAS' ? 'CANVAS CMD' : m}</button>`).join('') +
        `</div><div class="io-out" aria-live="polite"></div>` +
        `<div class="io-in"><textarea rows="2" placeholder="" aria-label="Message to the Notebook"></textarea>` +
        `<div class="io-actions"><button class="io-sel" title="Insert the current Canvas selection">+ Selection</button>` +
        `<button class="io-send">Send</button></div></div>`;
      IO.outEl = body.querySelector('.io-out');
      IO.inputEl = body.querySelector('textarea');
      const ta = IO.inputEl;
      const setPh = () => { ta.placeholder = IO.mode === 'CANVAS' ? 'presentiate dog, relate dog canine, remove dog\u2026' :
        IO.mode === 'QUERY' ? 'resolve dog \u00b7 selection \u00b7 hypernyms of cat\u2026' : 'Write to ECHO, or type help'; };
      setPh();
      IO.outEl.innerHTML = IO.history.map(entryHTML).join('');
      IO.outEl.scrollTop = IO.outEl.scrollHeight;

      body.querySelectorAll('.mode').forEach(b => b.addEventListener('click', () => {
        IO.mode = b.dataset.mode;
        body.querySelectorAll('.mode').forEach(x => x.classList.toggle('on', x === b));
        setPh(); ta.focus();
      }));
      IO.outEl.addEventListener('click', (ev) => {
        const chip = ev.target.closest('.chip');
        if (chip) E.app.focusWord(chip.dataset.word, 'io-ref');
      });
      const send = () => {
        const text = ta.value.trim();
        if (!text) { ta.focus(); return; }
        if (E.app.send(text, IO.mode)) { ta.value = ''; autosize(); }
        ta.focus();
      };
      body.querySelector('.io-send').addEventListener('click', send);
      body.querySelector('.io-sel').addEventListener('click', () => {
        const words = E.store.state.selection.map(id => E.store.state.manifestations[id]).filter(Boolean).map(m => m.word);
        if (!words.length) { E.app.toast('Nothing selected on the Canvas'); ta.focus(); return; }
        const ins = words.join(', ');
        const s = ta.selectionStart ?? ta.value.length, en = ta.selectionEnd ?? ta.value.length;
        const pre = ta.value.slice(0, s), post = ta.value.slice(en);
        const glue = pre && !/\s$/.test(pre) ? ' ' : '';
        ta.value = pre + glue + ins + post;
        ta.focus();
        const c = (pre + glue + ins).length; ta.setSelectionRange(c, c);
        autosize();
      });
      function autosize() { ta.style.height = 'auto'; ta.style.height = Math.min(ta.scrollHeight, 120) + 'px'; }
      ta.addEventListener('input', autosize);
      ta.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter' && !ev.shiftKey && !coarse) { ev.preventDefault(); send(); }
      });
    },
    onClose() { IO.outEl = null; IO.inputEl = null; },
  });
})(window.ECHO = window.ECHO || {});
