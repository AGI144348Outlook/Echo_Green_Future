# MOD-0004 external discovery — batch 1

Date: 2026-10-04  
Module: `MOD-0004-safe-relative-entry-writer`  
Abstraction freeze commit: `a38b4f6e99de6c064c101fa81374576c07c5cbae`  
Batch result: **5 distinct repositories reviewed; 0 selected; cumulative program progress 20/1,000**

## Review order

The source was preserved, generalized, tested and committed before external search. Only then were current issues inspected. Root licensing and contribution guidance were checked next, followed by present implementation, maintenance, duplication and adaptation feasibility.

No compatibility claim is made. Echo's source license snapshot omits the complete AGPL-3.0 text and adds use restrictions, so outbound compatibility remains a prerequisite decision even where a target has a clear license.

## Repositories 16–20

| # | Repository and issue | Issue and implementation fit | License/guidelines and maintenance evidence | Decision |
|---|---|---|---|---|
| 16 | [`ZJONSSON/node-unzipper#353`](https://github.com/ZJONSSON/node-unzipper/issues/353) | Open issue reports prefix-string traversal in JavaScript extraction. Current `master` no longer uses the reported `indexOf` check: `lib/extract.js` normalizes backslashes and gates with `path.relative`, rejecting empty, `..`-prefixed or absolute relative results. Package version is now 0.12.5 while the issue names versions through 0.12.3. | Root MIT license; no root or `.github` contribution guide found. Active refactor commit `431c45c` dated 2026-07-05. | Reject: issue appears stale against current code; MOD-0004 would duplicate a stronger native filesystem-aware check and lacks symlink handling. |
| 17 | [`ModOrganizer2/modorganizer#2304`](https://github.com/ModOrganizer2/modorganizer/issues/2304) | Open C++/Windows issue shows a drive-prefixed archive entry escaping the intended directory. A maintainer rejects the security framing but acknowledges the destination behavior as a bug. Correct work must fit Mod Organizer's archive/install pipeline and its chosen drive-path mapping, not transplant a browser-handle writer. | Root GPL-3.0 text; no root or `.github` contribution guide found. Active commit `efe2a02` dated 2026-07-08. | Reject: language/API mismatch and unresolved expected semantics; MOD-0004 contributes only the general reject-before-write principle. |
| 18 | [`fynyky/elemental#90`](https://github.com/fynyky/elemental/issues/90) | Open issue concerns `extract-zip` 2.0.1 reachable only through a transitive development dependency. The repository uses Playwright rather than the vulnerable Puppeteer path during normal tests. Correct remediation is upstream dependency removal/update or reachability reduction, not a new local entry writer. | Root `LICENSE.md` is MIT; no contribution guide found. Recent dependency merge `1162335` dated 2026-07-14. | Reject: dependency-management issue with no direct module integration point. |
| 19 | [`scanny/python-pptx#1137`](https://github.com/scanny/python-pptx/issues/1137) | Open Python issue alleges traversal through `PackURI`, directory reads and ZIP member writes. Current code accepts any leading-slash `PackURI`, joins `membername` for directory reads and writes that member name to ZIP. A correct fix needs OPC-specific URI canonicalization and compatibility tests; MOD-0004's policy is conceptually useful but JavaScript/browser-specific. | Root MIT license; no root or `.github` contribution guide found, and the issue reports no `SECURITY.md`. Latest repository commit found is `278b47b` dated 2024-08-07; the June 2026 issue has no maintainer response. | Deferred watch, not selected: credible policy overlap, but stale maintenance signal, domain-specific compatibility risk and Echo licensing remain blockers. |
| 20 | [`langchain-ai/langgraph#7871`](https://github.com/langchain-ai/langgraph/issues/7871) | Open Python CLI hardening issue requests a safe extractor before `ZipFile.extractall`. Current main still uses `extractall(path)`, but PRs #7870 and #7873 already contain the proposed helper and were auto-closed because the contributor was not assigned. The issue comment requests assignment to reopen the same patch. | Root MIT license; no root or `.github` contribution guide found at checked paths. Highly active main; commit `9a0394d` dated 2026-10-03. | Reject: direct technical fit but duplicate implementation already exists; contribution admission, assignment and Python-specific tests—not another code transplant—are the missing steps. |

## Selection result

Zero repositories were selected for a new upstream proposal.

`python-pptx#1137` is retained as a policy-level watch candidate, not as a selected target. Any sound contribution would need package-URI canonicalization tests, directory-read confinement and ZIP-member rules that preserve valid OPC relative references. MOD-0004 does not supply that Python/domain adaptation.

`langgraph#7871` is not a candidate because two materially identical patches already exist. Duplicating them would add review load without value.

## Resume state

- Distinct repositories reviewed: **20 / 1,000**.
- Next ordinal: **21**.
- Continue MOD-0004 discovery with discrete browser File System Access, offline import or archive-entry planning issues where no native fix or existing patch already covers the gap.
- Retain `python-pptx#1137` as an unselected, licensing-blocked and maintenance-sensitive watch candidate.

