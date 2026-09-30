'use strict';
// The initial surface intentionally contains no controls or content.
const worker = new Worker(new URL('python-worker.js', document.currentScript.src));
let nextId = 0;
const pending = new Map();
worker.onmessage = ({data}) => {
  const request = pending.get(data.id);
  if (!request) return;
  pending.delete(data.id);
  data.ok ? request.resolve(data.result) : request.reject(new Error(data.error));
};
worker.onerror = event => {
  for (const request of pending.values()) request.reject(new Error(event.message));
  pending.clear();
};
function call(op, code) {
  return new Promise((resolve, reject) => {
    const id = ++nextId;
    pending.set(id, {resolve, reject});
    worker.postMessage({id, op, code});
  });
}
const ready = call('init');
ready.catch(error => console.error('Pyodide initialization failed', error));
window.DevSuite = Object.freeze({ready, run: async code => {await ready; return call('run', code);}});
if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(console.error);
