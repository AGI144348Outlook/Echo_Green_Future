# MOD-0001 application review — 2026-10-02

The new `chat-archive-pyodide-workbench` branch exposes a concrete additional application for the Verified Resource Gate.

A browser-local archive workbench should not enable extraction or export merely because a file has been selected. It can model required resources such as:

- Pyodide runtime loaded;
- workspace directory permission granted;
- ZIP central-directory parser present;
- path-normalization and traversal rejection installed;
- extraction quota configured;
- output writer verified.

Only after the declared layout is instantiated and verified should extraction controls be enabled. If any required resource changes, the gate should revoke readiness and require re-verification.

This would improve initialization discipline, but it would not make archive contents trustworthy, turn browser directory permission into authentication, or replace ZIP-bomb limits, symlink/path traversal checks, quota enforcement and user confirmation.

Current branch evidence: `app.js@e0e476bc9c44436dc35e9894e8ca8bb8511bee6a` has Pyodide loading and directory selection but explicitly states that ZIP directory parsing and the Pyodide fallback are not implemented. The application is therefore prospective, not a claim that the branch already has a verified extraction gate.

