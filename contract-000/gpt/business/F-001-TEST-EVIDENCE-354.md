# F-001 — independent Run 354 byte-consistency evidence (2026-10-25 ~14 CT)

**Sole continuing income project:** F-001 TAM Protocol ebook; status **HOLD / NOT LAUNCH-READY**. Continuation of Run 353, not a new business pipeline. Public-only synthetic inputs; no private Testament or customer data.

**Prospective PRE:** [Issue #53 comment 6401820548](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6401820548), before testing. **Actual POST:** [same Issue comment 6401856208](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/53#issuecomment-6401856208), after testing.

## Exact sources and method

- New verifier `F-001-BUNDLE-BYTE-VERIFY-354.py` Git blob SHA-1 `35cd2704977e27f71529de3024a1b5d22612c888`, committed by `76ce1495414db8a23f9bf5f0e96ae93c18db72b7`.
- New harness `F-001-BUNDLE-BYTE-TEST-354.py` blob `d28f1c3d41dbb9ef60fb40c27ac02733d955b8cb`, commit `ee99a7f4d1d61c0e36374bb747aeea4bf57a87a8`.
- Imported prior shape gate `F-001-PACKAGE-EVIDENCE-GATE-353.py` blob `a5d3535860a488af090f3b25cc72fcd347ef0aef`.
- Raw GitHub retrieval in the local Linux container failed DNS. The three sources were reconstructed locally and **independently verified byte-identical to the GitHub blob SHA-1** before execution; no source edits between matching and test.
- Command: `python3 -I -B F-001-BUNDLE-BYTE-TEST-354.py` from a disposable Linux folder. Synthetic fixture files only, no TAM source download or CI.

## Observed outcomes (EXECUTION-VERIFIED synthetic)

**11/11 PASS.** Internally consistent synthetic manifest/bundle accepted only as `BYTE_CONSISTENT_ONLY` and `release=HOLD`. The ten negative cases all rejected: wrong externally supplied manifest pin, modified EPUB bytes, missing PDF, EPUB symlink, missing rights evidence file, modified rights evidence, modified staging receipt, sparse oversized PDF, malformed JSON manifest, and `release=READY` manifest. All accepted outputs state `publication_authorized=false`; no release authorization was generated.

The verifier uses fixed file names, opens the bundle root directory with `O_DIRECTORY|O_NOFOLLOW`, opens each file relative to that directory fd with `O_NOFOLLOW|O_NONBLOCK`, requires regular files, streams bounded SHA-256, compares EPUB/PDF declared byte sizes, and checks all 11 content hashes. The manifest SHA-256 must match a separate caller-supplied value.

## Interpretation and limits

This establishes **internal byte consistency**, not independent provenance: the same untrusted person could supply both the bundle and its pin. It does not validate JSON report semantics, actual EPUB/PDF conformance, EPUBCheck/Ace outputs, claims, licence, author identity, editorial approval, independent TAM rebuild or the authenticity of a stage receipt. The positive fixture intentionally uses DRAFT JSON evidence and synthetic non-EPUB/non-PDF bytes. Fixed-basename `O_NOFOLLOW` does not protect every ancestor path, and before/after fstat cannot prove absence of all concurrent modification races. Actual TAM end-to-end integration, real package checks and CI are **NOT RUN**.

**Next:** independently source the real F-001 package and a separately trusted manifest pin; verify real report semantics and package formats; compare a source-pinned independent rebuild; seek Claude's independent review. Continue F-001 only, HOLD pending Timothy's editorial/rights and explicit publication approval. No account, spending, outreach, payments, publication, paid API inference or Cloudflare loop.
