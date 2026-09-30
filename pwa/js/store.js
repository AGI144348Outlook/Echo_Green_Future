/* CanvasStore: authoritative shared Canvas state.
   C_{t+1} = Reduce(C_t, O_t). One reducer, two actors (user, echo).
   The view (pan/zoom) is workspace state, not Canvas semantics, so it is
   kept outside the reducer and never logged. */
(function (E) {
  'use strict';
  const S = E.store = {
    state: empty(),
    view: { x: 0, y: 0, scale: 1 },
    log: [],            // every attempted operation, applied or rejected
    listeners: [],
    seq: { man: 1, op: 1 },
    subscribe(fn) { this.listeners.push(fn); },
    newManId() { return 'man:' + (this.seq.man++) + '-' + Date.now().toString(36); },
    dispatch,
    reduce,
    replay,
    snapshot,
    load,
  };

  function empty() {
    return { manifestations: {}, relations: {}, selection: [] };
  }

  function permitted(state, op) {
    // ECHO may not move or remove what the person placed.
    if (op.actor === 'echo' && (op.op === 'MOVE' || op.op === 'REMOVE')) {
      const m = state.manifestations[op.target];
      if (m && m.actor !== 'echo') return 'ECHO may not ' + op.op.toLowerCase() + ' a user Presentiation';
    }
    return null;
  }

  // Pure: returns [nextState, errorOrNull]. Never mutates `state`.
  function reduce(state, op) {
    const a = op.args || {};
    const denied = permitted(state, op);
    if (denied) return [state, denied];
    switch (op.op) {
      case 'PRESENTIATE': {
        const word = String(a.word || '').trim().toLowerCase();
        const id = a.manifestationId;
        if (!word) return [state, 'PRESENTIATE needs a word'];
        if (!id) return [state, 'PRESENTIATE needs a manifestationId'];
        if (state.manifestations[id]) return [state, 'manifestation id already exists'];
        const x = Number(a.x), y = Number(a.y);
        const m = {
          id, word, canonicalId: a.canonicalId || ('word:' + word),
          renderer: a.renderer === 'lattice' ? 'lattice' : 'circle',
          x: isFinite(x) ? x : 0, y: isFinite(y) ? y : 0, actor: op.actor,
        };
        return [{ ...state, manifestations: { ...state.manifestations, [id]: m } }, null];
      }
      case 'MOVE': {
        const m = state.manifestations[op.target];
        const x = Number(a.x), y = Number(a.y);
        if (!m) return [state, 'no such manifestation'];
        if (!isFinite(x) || !isFinite(y)) return [state, 'MOVE needs numeric x, y'];
        return [{ ...state, manifestations: { ...state.manifestations, [m.id]: { ...m, x, y } } }, null];
      }
      case 'SET_RENDERER': {
        const m = state.manifestations[op.target];
        if (!m) return [state, 'no such manifestation'];
        const r = a.renderer === 'lattice' ? 'lattice' : 'circle';
        return [{ ...state, manifestations: { ...state.manifestations, [m.id]: { ...m, renderer: r } } }, null];
      }
      case 'REMOVE': {
        if (!state.manifestations[op.target]) return [state, 'no such manifestation'];
        const mans = { ...state.manifestations }; delete mans[op.target];
        const rels = {};
        for (const [k, r] of Object.entries(state.relations)) {
          if (r.from !== op.target && r.to !== op.target) rels[k] = r;
        }
        return [{ manifestations: mans, relations: rels,
          selection: state.selection.filter(i => i !== op.target) }, null];
      }
      case 'RELATE': {
        const from = a.from, to = a.to, type = a.type || 'is-a';
        if (!state.manifestations[from] || !state.manifestations[to]) return [state, 'RELATE needs two existing manifestations'];
        if (from === to) return [state, 'cannot relate a manifestation to itself'];
        const key = from + '|' + type + '|' + to;
        if (state.relations[key]) return [state, 'relation already exists'];
        const rel = { id: key, from, to, type, label: a.label || type, actor: op.actor };
        return [{ ...state, relations: { ...state.relations, [key]: rel } }, null];
      }
      case 'SELECT': {
        const id = a.manifestationId;
        if (!state.manifestations[id]) return [state, 'no such manifestation'];
        let sel = a.exclusive ? [] : state.selection.slice();
        if (!a.exclusive && sel.includes(id)) sel = sel.filter(i => i !== id);
        else if (!sel.includes(id)) sel.push(id);
        return [{ ...state, selection: sel }, null];
      }
      case 'CLEAR_SELECTION':
        return [{ ...state, selection: [] }, null];
      case 'RESOLVE':   // read-only; logged for provenance
        return [state, null];
      default:
        return [state, 'unknown operation ' + op.op];
    }
  }

  function dispatch(op) {
    const entry = {
      id: 'op:' + (S.seq.op++), actor: op.actor || 'user', op: op.op,
      target: op.target || null, args: op.args || {}, ts: Date.now(),
      provenance: op.provenance || 'ui',
    };
    const [next, err] = reduce(S.state, entry);
    entry.result = err ? 'rejected' : 'applied';
    if (err) entry.reason = err;
    S.log.push(entry);
    if (S.log.length > 5000) S.log.splice(0, S.log.length - 5000);
    if (!err) S.state = next;
    for (const fn of S.listeners) { try { fn(entry); } catch (e) { console.error(e); } }
    return entry;
  }

  // Rebuild state from the applied operations only. Used to prove determinism.
  function replay(ops) {
    let st = empty();
    for (const op of ops) {
      if (op.result !== 'applied') continue;
      const [n, err] = reduce(st, op);
      if (!err) st = n;
    }
    return st;
  }

  function snapshot() {
    const st = S.state;
    return {
      manifestations: Object.values(st.manifestations).map(m => ({
        id: m.id, word: m.word, canonicalId: m.canonicalId, x: m.x, y: m.y, actor: m.actor })),
      relations: Object.values(st.relations).map(r => ({ from: r.from, to: r.to, type: r.type })),
      selection: st.selection.slice(),
    };
  }

  function load(data) {
    if (!data || !data.state) return false;
    S.state = { manifestations: data.state.manifestations || {}, relations: data.state.relations || {}, selection: [] };
    S.log = Array.isArray(data.log) ? data.log : [];
    S.seq.op = S.log.length + 1;
    if (data.view) S.view = data.view;
    for (const fn of S.listeners) { try { fn({ op: 'LOAD', actor: 'system', result: 'applied' }); } catch (e) { console.error(e); } }
    return true;
  }
})(window.ECHO = window.ECHO || {});
