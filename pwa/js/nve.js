/* Local NVE: this device's persistent workspace, in IndexedDB.
   Keys: canvas, layout:auto, layout:saved, overlay, outbox, io, settings, instance.
   Falls back to memory if IndexedDB is unavailable (private mode). */
(function (E) {
  'use strict';
  let dbp = null;
  const mem = new Map();
  function open() {
    if (dbp) return dbp;
    dbp = new Promise((resolve) => {
      try {
        const req = indexedDB.open('echo-nve', 1);
        req.onupgradeneeded = () => req.result.createObjectStore('kv');
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => resolve(null);
      } catch (e) { resolve(null); }
    });
    return dbp;
  }
  function tx(mode, fn) {
    return open().then(db => new Promise((resolve) => {
      if (!db) { const r = fn(null); return resolve(r && 'result' in r ? r.result : undefined); }
      try {
        const t = db.transaction('kv', mode);
        const req = fn(t.objectStore('kv'));
        t.oncomplete = () => resolve(req && 'result' in req ? req.result : undefined);
        t.onerror = () => resolve(undefined);
      } catch (e) { resolve(undefined); }
    }));
  }
  E.nve = {
    get(key) {
      return tx('readonly', s => s ? s.get(key) : { result: mem.get(key) });
    },
    set(key, value) {
      const v = JSON.parse(JSON.stringify(value));
      return tx('readwrite', s => s ? s.put(v, key) : (mem.set(key, v), {}));
    },
    del(key) { return tx('readwrite', s => s ? s.delete(key) : (mem.delete(key), {})); },
    clear() { mem.clear(); return tx('readwrite', s => s ? s.clear() : {}); },
  };
})(window.ECHO = window.ECHO || {});
