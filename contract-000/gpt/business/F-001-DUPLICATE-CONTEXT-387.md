# F-001 — seven duplicated editorial claims: adjacent-context comparison (Run387)

**Sole project:** F-001 TAM Protocol ebook. **State:** HOLD / NOT LAUNCH-READY; all 45 occurrence cards remain **UNREVIEWED**. **PRE-TEST:** [Issue #60](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/60), with prospective normalization and tool-test addenda before those tests. **Prior work:** Run386 preview/duplicate analysis and 45-card Run383 queue. **Source:** public `AGI144348Outlook/The-TAM-protocol` at `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`. No source or Run358 CSV edits.

## Source and method

Fetched three actual pinned source files through the GitHub connector and verified returned blob IDs: `Article 6` `662d745f0b9b41236d1053cdbaa9351f7c020dd0` (29 sentence units), `Article 10` `e82be564872f636662652d34dcb8d3437559f84f` (9), `Collective information` `710ad3cd4feeae7bafa329d7437a78df4c40cfa8` (299). The connector-side JS diagnostic mirrored the original shared Python `claim_scan.py` splitter: `(?<=[.!?])\\s+|\\n{2,}`, then compared each pair's exact sentence and its immediately preceding/following sentence. An independently pre-registered second pass removed U+200B–U+200D and U+FEFF and collapsed whitespace **for neighbor comparison only**. It did not modify source or candidate text.

| Pair (article → Collective) | Duplicate text equal? | Both raw neighbors equal? | Both normalized neighbors equal? |
| --- | --- | --- | --- |
| Article 6#S4 → #S153 | yes | yes | yes |
| Article 6#S23 → #S172 | yes | yes | yes |
| Article 6#S29 → #S178 | yes | **no** | **no** |
| Article 10#S3 → #S293 | yes | **no** | yes |
| Article 10#S4 → #S294 | yes | yes | yes |
| Article 10#S5 → #S295 | yes | **no** | yes |
| Article 10#S8 → #S298 | yes | yes | yes |

**Observed:** 7/7 exact sentence duplicates; 4/7 identical raw adjacent windows; **6/7 identical normalized adjacent windows**. Article 10's two raw differences are leading invisible U+200B on the neighboring `I.`/`II.` headings; they are formatting differences, not demonstrated factual context changes. **One substantive adjacency difference:** `Article 6#S29` ends its source document, while `Collective information#S178` is followed by another sentence beginning a subsequent discussion. That changes the local reading boundary, but does not itself prove the claim's meaning changes. These are **adjacent sentence** comparisons, not full paragraph/section or historical fact-checks.

## New reproducible HOLD-only tool

[Read-only pinned Python comparator](f001_duplicate_context_387.py) checks exact Git blob identities of the three local source files, rejects symlinks/path traversal and changed bytes, compares the seven fixed occurrence pairs, and returns only a JSON report with `status=HOLD` and `release_authorized=false`. [Twelve synthetic Python unittest cases](test_f001_duplicate_context_387.py) passed using `python3 -I -B -m unittest discover -v -s . -p 'test_f001_duplicate_context_387.py'`. The tool/test committed blobs `8722a1971a82d870e2499161f8af4452cf1e3c4a` / `faeae3e76d72bc1ade7786464b27d05cb1f02ab1` matched locally executed bytes. Controls cover equal windows, zero-width formatting, real word change, source end, mismatched duplicate text, invalid index, pinned fixture, tampered source, symlink, traversal and splitter.

**Critical limit:** the offline Python comparator was executed on **synthetic fixtures only**, not the actual three local TAM files; real-source comparison was GitHub-connector-side JavaScript. The original Python claim scanner was **not** replayed against all eight actual TAM sources. These tests establish neither editorial truth nor a release gate.

## Editorial and coordination implications

Keep all **45 occurrence-specific cards** and their original status. The seven pairs can share an evidence investigation, but the Article 6 end-of-document boundary deserves independent context review. The Article 10 zero-width differences should not be overstated as different scientific evidence. No card was marked reviewed, approved, cut or rights-cleared.

**Claude:** independently examine Article 6#S29 / Collective#S178 in their full section contexts and the four P1 duplicate groups; continue evidence-specific review and Article4/Gerah/rights. **GPT next:** original Python scanner against eight exact local TAM files and pinned 334→344→347→351 coordinator replay with tamper negatives when materialization is possible. **Timothy:** A1–A6/B1/B4/B6/C1 and publication authority remain open. **F-001 HOLD.**
