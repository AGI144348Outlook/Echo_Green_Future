# MOD-0007 assessment — Actor-Scoped Command Admission

## Source classification

\`pwa/js/widgets.js\` is executable browser JavaScript. It combines a useful actor/ownership command gate with DOM creation, pointer behavior, layout mutation and persistence-facing serialization. The branch claims six command/ownership checks but does not preserve an executable test file, so the registry adds independent source characterization rather than treating that claim as a test suite.

The source rejects unknown actors/types, absent targets, nonfinite movement, nonpositive resize, and selected Echo mutations of user-owned widgets.

## Generalized contract

The generalized module is a pure admission function over commands and caller-supplied registry snapshots. It performs no UI or resource mutation, returns stable denial codes and prevents an agent from claiming human ownership.

It also tightens a source gap: an agent reopening a human-owned resource is denied whenever a \`binding\` field is present, including \`null\`, rather than only when the value is truthy.

Dependencies: JavaScript standard runtime only.

## Limits

Principal identity and registry integrity are trusted inputs. The module does not authenticate callers, render UI, persist layouts, resolve registry references, audit downstream effects or sandbox content.

## Licensing disposition

Internal preservation and research only. The source-branch license references AGPL-3.0 without including the complete text and adds restrictions. Compatibility is not asserted.
