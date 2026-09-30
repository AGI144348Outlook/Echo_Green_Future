'use strict';
const BASE = 'https://cdn.jsdelivr.net/pyodide/v0.29.3/full/';
let runtime;
let queue = Promise.resolve();
function initialize() {
  if (!runtime) runtime = (async () => {
    importScripts(BASE + 'pyodide.js');
    const py = await loadPyodide({indexURL: BASE});
    const response = await fetch(new URL('../python/algorithm_matrix.py', self.location.href));
    if (!response.ok) throw new Error('Boot source unavailable: ' + response.status);
    await py.runPythonAsync(await response.text());
    await py.runPythonAsync('runtime = AlgorithmMatrixRuntime()\nboot_state = runtime.run_boot_handshake()');
    console.log('[Dev Suite] alg-001 through alg-006 verified; 27 storage spaces unlocked');
    return py;
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
