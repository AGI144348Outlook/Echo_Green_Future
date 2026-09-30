# Blank Pyodide development suite

The initial page is entirely white. Pyodide 0.29.3 initializes in a dedicated worker. `DevSuite.ready` reports initialization and `DevSuite.run('1 + 1')` provides a development API without adding UI. Worker execution is serialized. Practice Python memory is local to this page; it is not Echo or Cloudflare state.

Serve `pwa/` over HTTPS or localhost. The PWA shell is cached; Python initialization still requires the pinned CDN runtime. Offline Python support is not claimed. No panels, widgets, sensors, notebook content or persistent Python state are loaded.

This branch is source-only. Hosting configuration uses the distinct `echo-dev-suite` name; active PWA hosting is unchanged. Widget development belongs on `widgeting-experiment`.

Algorithm 001 now boots automatically. See [ALGORITHM_001.md](ALGORITHM_001.md) for the protocol, slot mapping and verification limits. Use `await DevSuite.bootState()` to inspect its state.
