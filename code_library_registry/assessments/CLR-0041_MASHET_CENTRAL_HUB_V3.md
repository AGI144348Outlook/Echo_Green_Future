# CLR-0041 — Mashet Central Hub v3

## Classification
Recovered offline Flask control center / Notebook-PWA integration ancestor / Assessed.

## Source
User upload mashet_hub_v3.py, RFC-0031 v1.0.

## Architecture
- Local Flask server.
- /process endpoint delegates to MashetEVE.process().
- /status reports EVE cells, NVEs, primitive registry, Da'ath deposits, curriculum stages and boot log.
- substrate-only fallback if EVE fails to load.
- standalone mobile-oriented HTML/JS frontend.
- staged Cartesian and Kabbalistic validation display.
- FractalGrid and Tree-of-Life visualizations.
- local geosensory registry.
- local communication terminal.

## Strong contribution
This is not another intelligence kernel. It is an integration/control surface around the EVE runtime.

That distinction is valuable for the current architecture:
Runtime truth stays in EVE/registries; Hub owns presentation, controls, status, and user interaction.

It is a strong historical ancestor of the current Notebook/control-center idea.

## Audit findings
The substrate fallback uses random template choices, so identical prompts can produce different prose without semantic-state change.

The UI's staged “validation” is partly presentation logic: JavaScript can mark gates verified after timers/log messages. UI badges must not be treated as runtime evidence.

The Earth Stats panel explicitly creates deterministic pseudo-statistics from a query hash; these are synthetic display values, not Earth measurements or external observations.

The file-assimilation UI logs that a registry was updated after a timeout, but that frontend message alone is not evidence of backend ingestion.

Tailwind is described as CDN styling, so “zero external APIs” is compatible with local intelligence but not literally zero network dependency if that CDN is used.

## Modern reconstruction
Hub -> typed ActionRequest -> EVE/Governor -> EvidenceRecord -> Hub rendering.

Never allow:
UI says VERIFIED -> system is verified.

Require:
EvidenceRecord -> status projection -> UI badge.

## Status
Assessed / Genuinely distinct integration artifact / Very high Notebook/PWA relevance.
