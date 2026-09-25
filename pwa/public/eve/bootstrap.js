// EVE + ECHO Classroom bootstrap.
globalThis.__EVE_RUNTIME__ = Object.freeze({
  environment: "EVE",
  visualState: "VOID",
  governor: null,
  classroom: { status: "loading", lesson: "L000" },
  python: { engine: "Pyodide", status: "loading" }
});

(async () => {
  try {
    const pyodide = await loadPyodide();
    const eveResponse = await fetch("./eve/inert_eve.py", { cache: "no-store" });
    const lobbyResponse = await fetch("./eve/classroom/lobby.py", { cache: "no-store" });
    const lessonResponse = await fetch("./eve/classroom/lesson_000.json", { cache: "no-store" });
    const glyphResponse = await fetch("./eve/classroom/glyph_registry.json", { cache: "no-store" });
    const runnerResponse = await fetch("./eve/classroom/l000_runner.py", { cache: "no-store" });
    if (!eveResponse.ok || !lobbyResponse.ok || !lessonResponse.ok || !glyphResponse.ok || !runnerResponse.ok) {
      throw new Error("EVE/Classroom substrate load failed.");
    }
    await pyodide.runPythonAsync(await eveResponse.text());
    await pyodide.runPythonAsync(await lobbyResponse.text());
    const assignment = await lessonResponse.json();
    const glyphRegistry = await glyphResponse.json();
    await pyodide.runPythonAsync(await runnerResponse.text());
    pyodide.globals.set("GLYPH_REGISTRY_JSON", JSON.stringify(glyphRegistry));
    pyodide.globals.set("ASSIGNMENT_JSON", JSON.stringify(assignment));
    const resultJson = pyodide.runPython("run_l000_json(ECHO_LOBBY, GLYPH_REGISTRY_JSON, ASSIGNMENT_JSON)");
    const l000Result = JSON.parse(resultJson);
    const lobbySnapshot = JSON.parse(
      pyodide.runPython("import json; json.dumps(ECHO_LOBBY.snapshot())")
    );
    globalThis.__EVE_RUNTIME__ = Object.freeze({
      environment: "EVE",
      visualState: "VOID",
      governor: null,
      classroom: {
        status: "ready",
        lesson: assignment.assignment_id,
        assignment: assignment,
        lobby: lobbySnapshot,
        glyphRegistry: { status: "ready", count: glyphRegistry.glyphs.length, source: glyphRegistry.source },
        result: l000Result
      },
      python: { engine: "Pyodide", status: "ready", version: pyodide.version }
    });
    globalThis.__EVE_PYODIDE__ = pyodide;
    console.info("ECHO Classroom L000 ready.", lobbySnapshot);
    globalThis.dispatchEvent(new CustomEvent("echo:l000-complete", { detail: l000Result }));
  } catch (error) {
    console.error("EVE/Classroom initialization failed.", error);
    globalThis.dispatchEvent(new CustomEvent("echo:l000-error", { detail: String(error && error.message ? error.message : error) }));
  }
})();