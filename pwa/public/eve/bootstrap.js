// Invisible browser-side runtime bootstrap.
// No Governor, agent loop, or autonomous population is created here.

globalThis.__EVE_RUNTIME__ = Object.freeze({
  environment: "EVE",
  visualState: "VOID",
  governor: null,
  python: {
    engine: "Pyodide",
    status: "loading"
  }
});

(async () => {
  try {
    const pyodide = await loadPyodide();
    const response = await fetch("./eve/inert_eve.py", { cache: "no-store" });
    if (!response.ok) throw new Error(`EVE substrate load failed: ${response.status}`);
    const source = await response.text();
    await pyodide.runPythonAsync(source);

    globalThis.__EVE_RUNTIME__ = Object.freeze({
      environment: "EVE",
      visualState: "VOID",
      governor: null,
      python: {
        engine: "Pyodide",
        status: "ready",
        version: pyodide.version
      }
    });
    globalThis.__EVE_PYODIDE__ = pyodide;
    console.info("EVE substrate ready; Governor absent; visual occupancy remains VOID.");
  } catch (error) {
    globalThis.__EVE_RUNTIME__ = Object.freeze({
      environment: "EVE",
      visualState: "VOID",
      governor: null,
      python: {
        engine: "Pyodide",
        status: "error",
        message: String(error)
      }
    });
    console.error("EVE substrate initialization failed.", error);
  }
})();
