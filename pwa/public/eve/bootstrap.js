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
    if (!eveResponse.ok || !lobbyResponse.ok || !lessonResponse.ok || !glyphResponse.ok) {
      throw new Error("EVE/Classroom substrate load failed.");
    }
    await pyodide.runPythonAsync(await eveResponse.text());
    await pyodide.runPythonAsync(await lobbyResponse.text());
    const assignment = await lessonResponse.json();
    const glyphRegistry = await glyphResponse.json();
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
        glyphRegistry: { status: "ready", count: glyphRegistry.glyphs.length, source: glyphRegistry.source }
      },
      python: { engine: "Pyodide", status: "ready", version: pyodide.version }
    });
    globalThis.__EVE_PYODIDE__ = pyodide;
    console.info("ECHO Classroom L000 ready.", lobbySnapshot);
  } catch (error) {
    console.error("EVE/Classroom initialization failed.", error);
  }
})();