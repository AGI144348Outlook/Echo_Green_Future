# MOD-0006 discovery batch — 2026-10-06

Abstraction freeze: `85e4fda147e7c01dad94c210d12c4e3fa7e603aa`.

Repositories 26–30 were reviewed after the freeze. Each review started from a current issue and then checked repository license, duplication, correctness scope, maintenance evidence and feasibility.

| # | Repository | Issue | Root license observed | Result |
|---:|---|---|---|---|
| 26 | `cdfmlr/pyflowchart` | [#28](https://github.com/cdfmlr/pyflowchart/issues/28) | MIT | Reject: PR #29 duplicates the requested match/case work. |
| 27 | `coetaur0/staticfg` | [#17](https://github.com/coetaur0/staticfg/issues/17) | Apache-2.0 | Reject/defer: true CFG exception/loop semantics exceed MOD-0006; repository activity is stale. |
| 28 | `Technologicat/pyan` | [#53](https://github.com/Technologicat/pyan/issues/53) | GPL-2.0 | Watch only: active and related, but ordered execution is outside the frozen lexical-outline contract and Echo licensing is unresolved. |
| 29 | `scottrogowski/code2flow` | [#95](https://github.com/scottrogowski/code2flow/issues/95) | MIT | Reject: PR #97 already addresses the issue; logging setup is not this module's function. |
| 30 | `Open-MBEE/sysml-toolkit` | [#9](https://github.com/Open-MBEE/sysml-toolkit/issues/9) | Apache-2.0 | Reject/defer: resolved SysML semantic-tree visualization is a different language and semantic layer. |

Actual reviewed count: 5 this batch; 30 cumulative. Selected proposals: 0. Next ordinal: 31.

License labels record files observed at review time; they do not assert compatibility with Echo. Echo's root license remains incomplete and internally contradictory.
