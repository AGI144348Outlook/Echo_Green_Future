# MOD-0006 proposal status — 2026-10-06

Selection: 0 repositories.

Five distinct repositories were reviewed issue-first after the abstraction freeze. None passed technical-fit, duplication, maintenance and licensing gates together.

| Ordinal | Repository issue | Disposition | Reason |
|---:|---|---|---|
| 26 | [cdfmlr/pyflowchart#28](https://github.com/cdfmlr/pyflowchart/issues/28) | Reject | Existing PR #29 already implements `match`/`case`; MOD-0006 is not a full flowchart engine. |
| 27 | [coetaur0/staticfg#17](https://github.com/coetaur0/staticfg/issues/17) | Reject/defer | Correct `AsyncFor`, `break` and `raise` handling requires true CFG semantics; latest repository commit observed was 2022-08-07. |
| 28 | [Technologicat/pyan#53](https://github.com/Technologicat/pyan/issues/53) | Watch only | Active project and closest conceptual fit, but requested execution ordering is not derivable reliably from a lexical outline; GPL-2.0-or-later also requires a resolved Echo licensing decision. |
| 29 | [scottrogowski/code2flow#95](https://github.com/scottrogowski/code2flow/issues/95) | Reject | Existing PR #97 addresses the logging side effect; issue is not a flow-outline gap. |
| 30 | [Open-MBEE/sysml-toolkit#9](https://github.com/Open-MBEE/sysml-toolkit/issues/9) | Reject/defer | Rust/SysML resolved semantic-tree ownership, references and cycles are outside the Python syntax-outline contract. |

No proposal folder was created for an external repository. No upstream PR, issue comment or outreach was made.
