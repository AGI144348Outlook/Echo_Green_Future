'use strict';
const BASE = 'https://cdn.jsdelivr.net/pyodide/v0.29.3/full/';
let runtime;
let queue = Promise.resolve();
function initialize() {
  if (!runtime) runtime = (async () => {
    importScripts(BASE + 'pyodide.js');
    return loadPyodide({indexURL: BASE});
  })();
  return runtime;
}
self.onmessage = ({data}) => {
  queue = queue.then(async () => {
    try {
      const py = await initialize();
      if (data.op === 'init') return postMessage({id:data.id, ok:true, result:{version:py.version}});
      if (data.op !== 'run' || typeof data.code !== 'string') throw new Error('Invalid Python request');
      let result = await py.runPythonAsync(data.code);
      if (result && typeof result.toJs === 'function') {
        const proxy = result;
        try { result = proxy.toJs({dict_converter:Object.fromEntries}); } finally { proxy.destroy(); }
      }
      postMessage({id:data.id, ok:true, result});
    } catch (error) { postMessage({id:data.id, ok:false, error:String(error)}); }
  });
};
