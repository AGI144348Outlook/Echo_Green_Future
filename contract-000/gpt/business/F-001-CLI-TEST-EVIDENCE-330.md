# F-001 — Run 330 source-pinned CLI JSON repair, actual test evidence (2026-10-24 CT)

**Sole continuing business project:** `F-001`, TAM Protocol research ebook. **DRAFT / HOLD / BLOCKED / NOT LAUNCH-READY**. Test protocol published prospectively in [Issue #49](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/49) **before execution**; [actual same-thread post-test](https://github.com/AGI144348Outlook/Echo_Green_Future/issues/49#issuecomment-6388255263). No other F-001 product, account, storefront, payment, outreach, or publication.

## Source pins and exact patch

- Previous GPT source: `contract-000-gpt-run329-20261024-1259:contract-000/gpt/business/F-001-PRECISION-AUDIT-328.js`, Git blob `8b6fdfd4fbd87f0243862654e4c27db31bc9f1e5` (local `git hash-object` reproduced).
- Patched GPT-only branch copy of **the same path**: Git blob `eeae51f9107d03a94e1b2dfbe9c2574267e18cee`. Exactly **one source character removed**, changing `+"\\\\n"` (literal backslash+n) to `+"\\n"` (real line feed) in the CLI's `process.stdout.write`. The exported `audit()` function was not edited. Previous branches/commits retain the old file for audit.
- Public `AGI144348Outlook/The-TAM-protocol` pinned commit `d46456a18fe412398d0ae37ec5a8c4eebb44e0c9`: Dataset A `Dataset A: The Eshtemoa Inventory (Forensic Weight Distribution)` 610 bytes, Git blob `b62c970a660e0a6685b58db1ef121690daa4fce7`; Dataset B `Dataset_B_Binary_Matrix.md` 646 bytes, Git blob `12ef0fc2df6a4f55b4db9c90c08e2d5fbcc493a4`. Source content fetched through connected GitHub; scratch files independently `git hash-object`-verified. Git hashes attest bytes, **not** authorship, rights, historical validity or provenance beyond that source.

## Executed locally (Node v22.16.0; no GitHub CI)

Reproducible commands on verified local source copies (the filenames are local scratch paths, not tracked source files):

```sh
node F-001-PRECISION-AUDIT-328.js A.txt B.txt > output.json
python -m json.tool output.json > /dev/null
# Negative controls: one-byte changed A source and only one argument
node F-001-PRECISION-AUDIT-328.js A-tampered.txt B.txt
node F-001-PRECISION-AUDIT-328.js A.txt
```

| Prospectively declared check | Actual observation | Result |
|---|---|---|
| Valid pinned sources produce exactly one parseable JSON document with LF | Exit 0, stdout **5,141 bytes**, LF-terminated, JSON parsed; stderr empty | PASS |
| Summary unchanged | A 6 rows / 3 direct matches; B 8 rows / 7 half-even matches; `gerah_unit_conflict=true`; `release=HOLD`; `readiness=BLOCKED` | PASS |
| Tampered source fails SHA gate | A first mass `136.98g` → `136.97g`; exit 1, `source blob mismatch at 0` | PASS |
| Wrong argument count fails | One input path; exit 1 with usage error | PASS |

**Total 4/4 PASS**, matching pre-test expectations. The previous script's trailing literal `\\n` defect was reported by Claude §135, then independently repaired and tested here. No unplanned check failures. This fixes only CLI JSON serialization; it does not establish the author's actual precision method. Earlier independent Run 329 source comparison remains **B 6/8 half-up, 7/8 half-even, 8/8 truncation** and A **3/6** displayed-percent matches; those counts were **not retested** as a three-method comparison in this Run 330 CLI diagnostic.

**Limits:** Node v22 local scratch only; no Windows, Android, Cloudflare, CI, EPUBCheck, PDF, accessibility, historical measurement, license or author-approved final package tested. The CLI still has the Run 328 filename, intentionally preserving the one-character change and old evidence lineage. Claude's §135 source analysis and independent re-execution remain separately attributed. No frozen race tests altered.

**Next:** Claude may independently verify the repaired CLI from the new GPT branch. Timothy's A1–A6/B6, Dataset A row 6/7 and *Gerah* dispositions, manuscript claims, rights and explicit publication approval remain blockers. Continue with [release acceptance plan](F-001-RELEASE-PACKAGE-330.md); do not release a product on a successful CLI test alone.
