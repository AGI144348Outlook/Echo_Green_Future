"""ECHO runtime package - the portable kernel that runs inside Pyodide.

Layout:
  echo/kernel     the Governor skeleton, verbatim from the repository (A-000 ... A-158)
  echo/operators  LHEA letter operators and A-174 inversion probes
  echo/matrix     the canonical Registry (residents, hypernyms, local overlay)
  echo/canvas     ECHO as a Canvas actor (IDENTIFY -> VALIDATE -> OPEN)
  echo/mcw        MCW message envelopes and outbox (no keys, no network calls)
  echo/bootstrap  boot() and the JSON entry points the JavaScript bridge calls
"""
__version__ = "0.1.0"
