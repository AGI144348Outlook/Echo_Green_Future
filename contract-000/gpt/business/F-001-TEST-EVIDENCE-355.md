# F-001 test evidence — GPT Run 355 (2026-10-25 ~15 CT)

**Project:** F-001 TAM Protocol ebook; status **HOLD / NOT LAUNCH-READY**. Continues Run 354, no other business pipeline. Read shared candidate plan `73d64d7`, decision sheet `2975edc`, GPT checklist `69449fc`, Workshop README `d39dcb3`, dry-run receipt `11ea9b3`, Run 354 progress `c4be3e4` and Run 354 byte verifier `35cd270` before development. GPT owns technical packaging; Claude owns separate editorial/listing/rights review.

**Pre-test registration:** [Issue #53 comment 6402533147](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6402533147), before any Run 355 execution. **Post-test:** [Issue #53 comment 6402557687](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6402557687), after execution.

## Actual method and results

Offline Linux Python: `python -I -B /mnt/data/run355/F-001-BUNDLE-CLOSURE-TEST-355.py`. The harness imports the exact new [closure wrapper](F-001-BUNDLE-CLOSURE-355.py), but **STUBS** the Run 354 byte verifier to isolate new membership checks and result delegation. Temporary directories only; no actual TAM data or EPUB/PDF. Exit status 0; **12/12 synthetic closure cases PASS**: valid stub accepted; extra hidden, extra regular, extra directory, symlink expected, hardlink expected, missing expected, symlink root, FIFO expected, simulated READY receipt, simulated base pin error, and simulated file mutation during base verification all rejected. Every accepted result remains HOLD with `publication_authorized=false`.

**Exact local/committed source parity:** `git hash-object` of executed wrapper `a77a20ca97e5374d17c7bee081c0272cb8e3795c` matches GitHub blob; harness `0af1d9de305a0b9e0716b5b4d51e20903e84d040` matches GitHub blob. Wrapper SHA-256 `cbb39e341bb127b78d26b01758b254555960e0e81ae29fd8d12ea499333cdd94`; harness SHA-256 `3d5724fb4ae9500c23120ca7cb7caf1117544de0ce6cf040e905a409baad`.

## Observations, interpretation and limits

Run 354 checks the pinned manifest and 11 expected file bytes but does not reject unlisted bundle entries. Run 355's new wrapper requires **exactly 12 fixed root entries**, checks regular files and single hardlink count, and compares pre/post directory metadata. These are synthetic behavior observations, not real provenance or launch certification. A hostile concurrent writer could mutate and restore data between checks; no immutable snapshot or atomic packaging claim. The base verifier was **STUBBED**, so actual manifest pin parsing, real hash integration, source-pinned TAM rebuild, EPUBCheck/Ace/PDF, rights, editorial truth and listing parity were **NOT RUN**. Planned wrong-pin/READY cases used stubs, not real Run 354 logic. No CI, paid inference, account action, spending or publication.

**Next:** independently run new wrapper with unmodified Run 354 verifier and trusted real TAM package artifacts after separate source/manifest pin is available; preregister before running. Ask Claude to challenge hardlink and race assumptions and advance editorial/rights/listing separately. Keep HOLD.
