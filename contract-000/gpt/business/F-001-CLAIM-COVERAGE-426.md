# F-001 TAM ebook — Run426 source-pinned claim inventory and trigger-coverage gap

**PRE:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/99; [prospective amendment before coverage tests](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/99#issuecomment-6478134127). **Sole business project:** F-001 TAM Protocol speculative research-notebook ebook, **HOLD / NOT LAUNCH-READY**. Original scanner `library-shared:Business/ideas/F-001-tam-build/claim_scan.py`, blob `31f3dcff486c4c8cc96d514eb425da86834d00c3`; exact eight public TAM source blobs listed in [machine-readable candidate manifest](F-001-SOURCE-PINNED-CLAIMS-426.json).

## Observation — eight actual public source files, byte-authenticated

Read all eight source texts through the authenticated GitHub connector at `AGI144348Outlook/The-TAM-protocol:main`; recomputed Git blob SHA-1 **from full UTF-8 bytes** using the dependency-free JS implementation and compared each to independent GitHub tree/blob pins: **8/8 matched**. The JS [candidate scanner](f001_claim_scan_parity_426.js) transcribes Python's eight file names, sentence split and four trigger patterns. It generated **42 candidates** (README 1; Article1 2; Article2 3; Color/Dental 3; Article5 3; Article6 3; Article10 4; Collective 23). Trigger totals: certainty **12**, percent **2**, accuracy **13**, superlative **20** (47 total labels because rows may have multiple). All 42 status fields are blank. The first README claim concerning `>95\\%` correlation is **not** an independently verified scientific result.

**Controls:** 29/29 passed in V8 on the **exact GitHub-committed JS source**: SHA-1 `abc` known vector, eight full Git-blob checks, row-count and distribution checks, positive manifest replay, and 14 tamper-negative cases covering altered rows, source content, pins, statuses, and release flags. This authenticates bytes and reproducibility of the JS transcription only; the **original Python scanner has NOT been executed against these eight files**, and Python/JS Unicode word-boundary differences remain possible. The original 42-row manifest is retained separately from all editorial review decisions.

## Newly observed original-scanner coverage gaps — exploratory second phase

The original `certainty` regex includes `prove[sd]?` but not `proving`. Its `percent` regex `\\d+(\\.\\d+)?\\s?%` misses source-escaped percentages such as `20\\%`. After a **prospectively posted amendment**, 9/9 synthetic/source assertions passed for adding `proving` and optional literal backslash before percent. On the same eight verified sources, this changes **four** sentence trigger-label sets, and identifies **two previously unselected sentences**:

- `The Color Dyed and Dental Records`, sentence 14: claim of a `20\\%` trade-value loss; original trigger set empty.
- `Collective information`, sentence 90: claim about `13.7\\%` of a circumference and a trade-wind interval; original trigger set empty.

Also changes trigger labels, without adding rows, for `README.md` sentence 24 (`proving` and `>95\\%`) and `Collective information` sentence 100 (`13.7\\%`). The **proposed enhanced scan would yield 44 candidates**, not 42, with no claim truth established. This is a regex-coverage observation; some other unsupported claims may still evade all four triggers.

**Proposed, NOT APPLIED to shared scanner:**

```diff
-    "certainty": r"\\b(prove[sd]?|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed)|establish(es|ed))\\b",
-    "percent": r"\\d+(\\.\\d+)?\\s?%",
+    "certainty": r"\\b(prove[sd]?|proving|proof|proven|confirm(s|ed)?|undeniabl[ey]|definitive(ly)?|certain(ly)?|irrefutabl[ey]|conclusive(ly)?|demonstrat(es|ed)|establish(es|ed))\\b",
+    "percent": r"\\d+(\\.\\d+)?\\s?\\\\?%",
```

This is a review candidate, not an applied patch or a verified Python regression. **All 82 existing editorial occurrences (45 baseline + 37 supplemental) remain UNREVIEWED.** Do not equate those 82 review locations with the scanner's 42/44 sentence candidates; sets overlap but have different provenance and selection criteria.

## Remaining acceptance / coordination

Original Python eight-source scanner execution, full dataset coordinator 334→344→347→351 and receipts, human historical/scientific/rights dispositions, final deterministic EPUB/PDF accessibility and Android checks, exact book identifier, listing terms, Timothy's A1–A6/B1/B4/B6/C1 decisions and explicit publication authorization all remain outstanding. Container direct GitHub DNS failed with `Temporary failure in name resolution`; no CI was triggered. **Claude:** independently review the two newly detected historical/quantitative claims and the scanner-regex proposal, alongside P1-F01/F07/F12; do not promote any claim to VERIFIED from regex matching. No accounts, outreach, publication, spending, payments, paid inference or Cloudflare loops.