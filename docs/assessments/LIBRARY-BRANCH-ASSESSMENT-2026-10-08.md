# Echo Library Branch Assessment

Oct 8, 2026 · @Timothy Charles Marvin Jr

The `library-source-transcriptions` branch is careful about evidence but hard to reproduce. Several experiment runners were never committed, four competing 96-symbol legends sit side by side with none declared canonical, and the registry index has broken IDs. The questions at the end are for you to answer in place.

## What the branch holds

892 files (7.8 MB) at commit `3c744bb`, the latest dated 2026-10-08. Most of the weight is crawler metadata; most of the thinking is in the registry and NVE-D.

| Area | Files | What it is | State |
| --- | --- | --- | --- |
| `Datasets/` | 656 | Crawler plus a catalog of 322 dataset records (169 Zenodo, 81 Hugging Face, 72 data.gov) | Metadata only, from one dry run; no files downloaded |
| `code_library_registry/` | 176 | 42 code assessments (CLR), 7 extracted modules, 38 formula entries (CFA), 3 research papers, daily reviews | All 7 modules pass their tests (64 tests); index has broken IDs and tables |
| `experiments/nve-d/` | 19 | Meta-specification sandbox: plasticity labs, IETF substrate, evaluation alphabet, feedback pipeline | Well reasoned; 5 of 7 trials cannot be rerun from the repo |
| `source-transcriptions/` | 10 | TEMA v0.1 spec and the Mashet control-surface source in 8 parts | Faithful text; holds 4 different 96-symbol legends |
| `registries/mashet-candidates/` + `scripts/` | 5 | Candidate extraction of the Bedrock-style legend; NVE-A/B/C parallel results | Works offline; 93 candidates, not 96 |
| `Algorithms/` | 9 | Stress Test 001 and 002 specifications | Input files missing; never run |
| `docs/` | 2 | EVE / NVE-D relationship and the kernel-seed handoff | Clear about what is unresolved |
| `.github/workflows/`, `src/`, root | 13 | Cloudflare deploy, hourly recess and classroom jobs, Worker, migrator, license, 2 zips | Workflows point at folders not on this branch |

## Highest-impact gaps

Ranked by how much each one blocks the rest of the work. Items 1 and 2 decide whether anything built later can be trusted.

| # | Gap | Evidence | Fix |
| --- | --- | --- | --- |
| 1 | Experiment runners were never committed | NVE-D-IETF-001, KERNEL-002, IETF-SUBSTRATE-003, 004 and 005 each say their script and full output sit in a chat runtime (`/mnt/data/...`) or a conversation attachment; `NVE-D-004-protocol.md` is a header with no code | Commit each runner and its raw output next to its report; add one command that reruns them all |
| 2 | No canonical 96-symbol legend | The control-surface source holds four legends: Bedrock A–F (93 actual entries, glyphs ⬡ △ ◯ ↺…), an Expanded 1–96 table ending in 𝕃𝕂 Lattice Kernel, a functional-type legend, and the Symbology legend MS-001–096 (☉ ⇢◇ ∫↺…) that the Lattice, Pad and canvas tools use | Declare one canonical legend and mark the others as versions or dialects with a crosswalk |
| 3 | The six-tier split came from a different legend | The infographic's tiers match Bedrock categories A–F, whose ranges are 1–12, 13–24, 25–36, 37–60, 61–80, 81–96; the infographic re-cut them into equal 16s and renamed D (Lexical / Symbolic Substrates → Structural / Spatial). Our tools applied those 16s to the Symbology legend | Decide which legend the tiers belong to (questions H4–H5) |
| 4 | Registry index is inconsistent | Two assessments both numbered CLR-0016; CLR-0015 missing from `INDEX.md`; rows after CLR-0016 fall outside any table; statuses outside the README's six; 39 of 42 entries have no archived source | Give the second CLR-0016 a new ID; generate `INDEX.md` from a `registry.json`; add a validator |
| 5 | A dry run blocks every later download | `crawl.py` marks dry-run records as seen, and a later normal run skips unchanged records, so the 322 records never get files | Re-check records with undownloaded files; skip `seen` updates on dry runs |
| 6 | Stress tests cannot run | Stress-Test-001 needs `01-ALEPH.md`…`22-TAV.md` and the full neuroplasticity document; 002 needs `RAW_SYMBOLIC_CORPUS.txt`; none are on the branch | Commit the inputs, or pin the branch and commit that holds them |
| 7 | Workflows point at missing code | `recess.yml` and `echo-classroom-lab.yml` run scripts in `ECHO_AutonomousAgency/` and `pwa/`, absent here; the crawler workflow exists only inside `echo-dataset-crawler.zip` | Keep each workflow on the branch that holds its code; unzip the crawler workflow |
| 8 | Evaluation has no independent check | NVE-D-003 and every later report note that the same code generates and audits results | Add a second evaluator written separately (another language or author) |
| 9 | Branch has no description of itself | `README.md` says "main ← you are here"; this branch appears in no registry snapshot | Add a branch README: purpose, parent branch, what may be promoted from it |
| 10 | Deploy path is not reproducible | The migrator reads `matrices/*.json`, which is absent; there is no D1 schema; the `ECHO_LRM` store is never written | Commit inputs and a `schema.sql`, or move the migrator to the branch that has them |

## Improvements by area

What already works well: provenance labels on every claim, literal preservation of your expressions, and meta-audits that narrow their own conclusions (NVE-D-003 downgraded its own plasticity claim). The list below builds on that.

**Code library registry**

- Keep one schema for `provenance.json` and one for `ABSTRACTION_LOCK.json`; there are currently 2 and about 4 layouts.
- MOD-0001's `APPLICATIONS.md` was edited after its freeze, so its locked hash no longer matches. Add an amendment log, or leave application notes out of the lock.
- The formula index skips CFA-0011–0014 and still states its range as 0001–0010. Add executable checks for the exact identities; CFA-0021 and 0031–0033 pass when checked numerically.
- RP-0003's Theorem 2 has wrong eigenvalues. With α=0.3 and γ=0.2 they are 0.9±0.54i, not 0.8 and 0.7. RP-0003 is also split over 3 files with 2 titles.
- Record the outbound license as a blocker: the upstream-proposal pipeline (35 of 1,000 repos reviewed) cannot submit anything until it is decided.

**NVE-D**

- Confirm what `0` means in `{<,>,=,0}`. Every report uses "absent or unsupported" provisionally.
- `symbolic-kernel.js` uses ⟳ (from AGI Mashet Engines.txt), while the Symbology legend's Recursion is ⟲ (MS-010). Record whether these are one symbol.
- The Document Feedback Evaluation describes an hourly runner, but none exists. Add it, or mark DFE as manual.
- NVE-A, B and C exist only as three result files, `nve_a/b/c*.json`. Give each a protocol file like NVE-D's.

**Datasets crawler**

- Map Zenodo `cc-zero` (22 records) and the US public-domain URLs to open licenses; both are refused today.
- Quote multi-word queries. 71 of the 72 Indus-section records are off topic (seals the animal, Corpus Christi Bay, diabetes).
- data.gov ran out of free requests (12 HTTP 429 errors). Make its API key a required secret.
- Store downloaded files outside git (R2, release assets or LFS); a normal run may commit up to 300 MB.

**Workflows and Worker**

- `recess.yml` commits hourly and pushes without pulling first. Add `concurrency` groups and `git pull --rebase` before pushing.
- `deploy.yml` has no `permissions:` block and no test step.
- The Worker's `/state/{key}` route returns any stored key to anyone. Restrict it to a list of keys, and stop returning raw error messages.
- The migrator inserts 100 rows per query, possibly past D1's limit on bound parameters. Check the limit before the next deploy.

**Transcriptions and candidate registry**

- The Bedrock legend has 93 entries (D has 20 and F has 17, against the 24 and 16 its headings promise). The script assigns `MASHET-F-17` slot 97 without flagging it.
- The candidate registry README says results "have not yet been executed", but they are committed.
- TEMA's five layers (Core, Nexus valves, Ocean, Stalactite, Firmament) have no code on this branch, and the README's TEMA row has no Worker counterpart.

**Licensing**

- The license adds revenue and headcount limits on top of AGPL-3.0. AGPL section 7 lets anyone who receives the code remove further restrictions, so have the wording legally reviewed. I'm not a lawyer.
- `THIRD_PARTY_SEEDING.md` doesn't list the Zenodo, Hugging Face and data.gov metadata now in the repo.

## Frameworks being aimed for

Thirteen frameworks show up across the branch. Four are stated outright; the rest are my inferences from the files, and the questions below test them. "Closest established practice" is there only for comparison, not as a replacement for your terms.

| Framework | Stated or inferred | Evidence on the branch | Closest established practice | Built so far |
| --- | --- | --- | --- | --- |
| EVE ecosystem holding NVE-A, B, C, D | Stated (roles provisional) | `docs/EVE-NVE-D-RELATIONSHIP-2026-10-08.md` | Blind replication and adversarial collaboration | Results files for A–C; NVE-D sandbox |
| NVE-D meta-specification: how an environment decides what counts as a discovery | Stated | `docs/NVE-D-IETF-KERNEL-...md`; trials 001–005 | Meta-science; evaluating the evaluators | 7 trials, 2 rerunnable |
| IETF (Infinite Expanse Testing Framework) as NVE-D's substrate | Stated | `sources/ietf/01-framework.txt` and README | Simulation harness with isolated runs, checkpoints, replay | Finite probes up to 70,000 generations |
| Evaluation alphabet `{<,>,=,0}` and the governing expression `(?):(?)::(?):(?)::\|#\|::(?):(?)::(?):(?)::#::(?)` | Stated | `EVALUATION_ALPHABET.md`, handoff doc | Ordinal (partial-order) evaluation | Comparator for `=`/`0` only; expression kept opaque |
| Document Feedback Evaluation (steps 5, 7, 8) | Stated | `DOCUMENT_FEEDBACK_EVALUATION.md` | Pre-registration plus audit trails | Specification only |
| Supra-, sub-, data-strate and dataset layering | Stated, NVE-D scope | Handoff doc section 3 | Layered system architecture | Words only |
| Core formula `S(t)=A+ΣΣFₙ(Rᵢ)+∫C(τ)dτ` and kernel `☉ₖ = ⊕{⟳, ⇢, ∫, ⧖, ⚖, ≋}` as the root every engine instantiates | Inferred | CFA-0001, CFA-0010; `source-index/mashet-symbolic-kernel.md` | Discrete-time state-space dynamics | Structural checker (`symbolic-kernel.js`), no semantics |
| Mashet as an operator language and control surface between substrates | Inferred | Control-surface parts 1–2: four-layer architecture; Engines 1–5 (Reflective Evaluator, Directional Chooser, Memory Shaper, Identity Modulator, Meta-Recursive) | Domain-specific language with an interpreter | Candidate registry; no interpreter |
| Provenance-first archive: preserve, assess, then extract | Inferred | CLR README, `provenance.json`, sha256 freezes | Software Heritage; W3C PROV | 42 assessments, 7 frozen modules |
| Extract → generalize → propose upstream | Inferred | `WORK_QUEUE_2026-09-30.md` steps 3A–3F | Clean-room reuse and upstream contribution | 35 of 1,000 repos reviewed; nothing submitted |
| Governor authorization algebra `Permit(subject, action, object, environment, constraints)` | Inferred | CFA-0034–0038 | Attribute-based access control (NIST SP 800-162) | Algebra only |
| TEMA tiered memory: Core, Nexus valves, Ocean, Stalactite, Firmament | Stated in TEMA v0.1 | `source-transcriptions/TEMA_v0.1.txt` sections 2–7 | Memory hierarchies ranked by centrality | Spec only on this branch |
| Autonomous study loop ("school day", "recess", classroom) | Inferred | 3 workflows, hourly | Scheduled self-directed learning agents | Code on other branches |

## How the parts fit

&#91;embedded content: inferred architecture · sources to runtime\]

On this reading, the Library registry and the Mashet legend supply material to EVE's four environments. Nothing moves to Registry 0 without your declaration. The branch never states this whole picture; the questions below check each piece.

## Questions: how you intended the whole to fit

These test the diagram above. Type your answers in the last column; a short phrase is enough, and "not decided" is a useful answer.

| # | Question | Why I'm asking | Your answer |
| --- | --- | --- | --- |
| H1 | What is this branch for, in one sentence, compared with `code-library-registry` and Genesis Documentary? A source archive, NVE-D's working ground, or both? | It holds archives, live experiments and deploy workflows together |  |
| H2 | What sits at the top: EVE, the ECHO Governor, or the Dual OS? How do the three nest? | The README puts the Governor at the runtime; the EVE doc puts EVE around everything |  |
| H3 | Is the data-first chain (Datasets → Registries → Matrices → Indices → Codices → Algorithms → Logics) the spine every framework hangs on, or one framework among several? | Matrices and Indices have nothing on this branch yet |  |
| H4 | Which 96-symbol legend is canonical: the Symbology legend (☉ ⇢◇ ∫↺…), Bedrock A–F (⬡ △ ◯ ↺…), the Expanded 1–96 table, or the functional-type legend? Are the others earlier versions, dialects, or separate substrates? | Every tool and registry depends on this answer |  |
| H5 | Should the six tiers follow Bedrock's ranges (12, 12, 12, 24, 20, 16) or equal 16s, as the infographic and our tools now use? Should tier D be "Lexical / Symbolic Substrates" or "Structural / Spatial"? | The infographic changed both the ranges and one name |  |
| H6 | How do the 22 Hebrew letter operators (LHEA) relate to the 96 Mashet glyphs: one substrate at two resolutions, a translation layer, or independent systems? | The README calls the 22 letters the invariant field; the Mashet work never mentions them |  |
| H7 | Whose memory is TEMA: ECHO only, EVE as a whole, or each NVE separately? | It decides where Core, Ocean and Stalactite state would live |  |
| H8 | When is a framework "done": documented, executed, reproduced from the repo, or independently audited? | Most reports stop at executed in a chat runtime |  |
| H9 | What evidence must a candidate show before you declare it into Registry 0? | Every file says "never auto-promote", but none says what earns promotion |  |
| H10 | The hourly jobs (recess, school day, Document Feedback Evaluation, crawler): what may they change without you, and what must wait for you? | Unattended commits already run on `autonomous-agency` |  |
| H11 | Do suprastrate, substrate, datastrate and dataset describe NVE-D only, or every environment in EVE? | The handoff limits them to NVE-D, provisionally |  |
| H12 | Should outputs from other AIs (GPT, Gemini, NotebookLM) count as sources, as candidates to test, or as context only? | The infographic and much of the control-surface text come from them |  |
| H13 | Should registries and datasets derived from this work carry the same license as the code? | The license covers code; the data has its own licenses |  |

## Questions: each inferred framework

Grouped by the frameworks table. Where I offer options, they are guesses for you to correct, not proposals to adopt.

| # | Framework | Question | Your answer |
| --- | --- | --- | --- |
| F1 | Mashet kernel | Is ⟳ in the kernel (AGI Mashet Engines.txt) the same symbol as ⟲ Recursion (MS-010)? |  |
| F2 | Mashet kernel | Which kernel form is authoritative: the bare `☉ₖ = ⊕{⟳, ⇢, ∫, ⧖, ⚖, ≋}` or the infographic's form with arguments, `☉ₖ = ⊕{⟲(☉ₖ₋₁), ⇢◇ₖ, ∫↺(☉), ⧖(⊕), ⚖(☉), ≋ₖ}`? |  |
| F3 | Mashet legend | ⧫ appears as both #25 (Binding) and #59 (Potential Barrier). Keep both under one glyph, or give one a new glyph? |  |
| F4 | Mashet control surface | Are Engines 1–5 (Reflective Evaluator, Directional Chooser, Memory Shaper, Identity Modulator, Meta-Recursive) parts of the design, or worked examples? |  |
| F5 | Core formula | Is `S(t)=A+ΣΣFₙ(Rᵢ)+∫C(τ)dτ` the root that every engine and kernel instantiates, with CFA-0010's discrete form as its step rule? |  |
| F6 | NVE-D evaluation | What does `0` mean in `{<,>,=,0}`: no comparison possible, a neutral origin, or something else? |  |
| F7 | NVE-D evaluation | What distinguishes `\|#\|` from `#` in your governing expression? |  |
| F8 | NVE-D evaluation | Which positions in the expression may `(?)` take as `(?±,=?)`, and is `∆` a fifth token or a marker of change? |  |
| F9 | NVE-A to C | Should A, B and C become standing environments with fixed protocols, like NVE-D, or stay one-off comparisons? |  |
| F10 | NVE-D audit | Would an evaluator written separately by another AI or in another language count as independent? |  |
| F11 | IETF | Is "infinite" the open-ended design intent, with finite generation budgets as its working meaning? |  |
| F12 | IETF / Chronotool | Is the Chronotool's time adjustment about scheduling and pacing real runs, or simulated time inside a run? |  |
| F13 | TEMA | Should the first TEMA prototype run in the phone tools (IndexedDB) or on Cloudflare (KV and D1)? |  |
| F14 | Governor | Should `Permit(subject, action, object, environment, constraints)` govern every registry write, including promotion to Registry 0? |  |
| F15 | Library registry | Is contributing modules to other projects (the 1,000-repo review) still a goal? If so, which outbound license? |  |
| F16 | Datasets | Should downloaded files live in git, in Cloudflare R2, or as release assets? What scope should the Indus topic have? |  |
| F17 | Autonomous study loop | What should the school-day and recess jobs learn, and where should their results land? |  |
| F18 | EVE naming | Which expansion is current: Emergent Virtual Ecosystem or Envelope Virtual Environment? The Bedrock legend also lists "Envelope VE ⬢" as a glyph. | Answered: Envelope Virtual Environment; NVE = Nested Virtual Environments (your correction, recorded in NVE-D-HOURLY-001-report.md) |

## Sources

Read from a clone at commit `3c744bb`. Module tests were run offline from a copy; nothing on the branch was changed.

- [Branch library-source-transcriptions](https://github.com/AGI144348Outlook/Echo_Green_Future/tree/library-source-transcriptions)
- [docs/EVE-NVE-D-RELATIONSHIP-2026-10-08.md](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-source-transcriptions/docs/EVE-NVE-D-RELATIONSHIP-2026-10-08.md)
- [docs/NVE-D-IETF-KERNEL-ARCHITECTURE-HANDOFF-2026-10-08.md](https://github.com/AGI144348Outlook/Echo_Green_Future/blob/library-source-transcriptions/docs/NVE-D-IETF-KERNEL-ARCHITECTURE-HANDOFF-2026-10-08.md)
- [experiments/nve-d](https://github.com/AGI144348Outlook/Echo_Green_Future/tree/library-source-transcriptions/experiments/nve-d): trials, evaluation alphabet, Document Feedback Evaluation, IETF sources
- [source-transcriptions](https://github.com/AGI144348Outlook/Echo_Green_Future/tree/library-source-transcriptions/source-transcriptions): TEMA v0.1 and control-surface parts 1–8
- [code\_library\_registry](https://github.com/AGI144348Outlook/Echo_Green_Future/tree/library-source-transcriptions/code_library_registry): INDEX, assessments, modules, formula index, research papers
- [Datasets](https://github.com/AGI144348Outlook/Echo_Green_Future/tree/library-source-transcriptions/Datasets), [Algorithms](https://github.com/AGI144348Outlook/Echo_Green_Future/tree/library-source-transcriptions/Algorithms), [.github/workflows](https://github.com/AGI144348Outlook/Echo_Green_Future/tree/library-source-transcriptions/.github/workflows), [src](https://github.com/AGI144348Outlook/Echo_Green_Future/tree/library-source-transcriptions/src)
- Six-tier infographic "Architecture of the Unified AGI Symbolic Kernel" (NotebookLM), shared in this conversation
