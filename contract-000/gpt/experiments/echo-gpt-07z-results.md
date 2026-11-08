# Echo-GPT 07Z post-execution evidence — Issue #349
Preregistered before execution: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/349. Source commit a78727548fbb05e868a260995bd0942e7adf7065, retrieved Git blob 6c438fe6995861b446517a5622beff56b598ee76. Executed fetched JavaScript as an expression in isolated V8 (not Node CLI). Seeds 3301, 3302, 3303, 3304. No CI, paid inference, network effects or canonical changes.

| Type | Passed / attempted | Interpretation limit |
|---|---|---|
| T1 unique identities | 4/4 | Static 27-character list; no adversarial mutation |
| T2 separate-run replay | 4/4 | Same-process function re-instantiation, not cross-process |
| T3 rotated occupancy | 4/4 | One-step index permutation, not moving physical rings |
| T4 two-ring order | 4/4 | Explicit expected indexed chars; related implementation |
| T5 three-ring order | 4/4 | Explicit expected indexed chars; related implementation |
| T6 radius bound | 4/4 | 32 analytic samples, no collision dynamics |
| T7 frozen A-000 alias | 4/4 | Synthetic frozen record; NOT Genesis actual mutable path |
| T8 neighbor intervention | 4/4 | Engineered local rule, no learned causal discovery |
| T9 coupled vs uncoupled | 4/4 finite metrics | Not a superiority pass; synthetic developer-visible target |
| T10 shuffled/reversed/no-op | 4/4 finite metrics | Not a superiority pass; controls measured |

40/40 implemented checks true, 0 false. Weaknesses: T9/T10 only assert finiteness; T4/T5 share indexing logic with prediction; T7 not an adversarial Genesis test; no independent sealed target, learning, lexicon or genuine dynamic ring boundary.

| seed | coupled MSE | uncoupled | shuffled | phase-reversed | no-op |
|---|---:|---:|---:|---:|---:|
| 3301 | .00229699434 | .00233761715 | .00228648038 | .00246547615 | .00102366405 |
| 3302 | .00184810074 | .00189993586 | .00184579128 | .00195405293 | .00102366405 |
| 3303 | .00143063841 | .00148387849 | .00143497570 | .00147638188 | .00102366405 |
| 3304 | .00106027816 | .00110595885 | .00106886542 | .00105920087 | .00102366405 |

Observation: coupling beats uncoupled 4/4 but loses to no-op 4/4, beats shuffled 2/4 and phase-reversed 3/4. Intervention +.4 at cell 13 changes cell 12 +.01 and cell 0 +0. Interpretation: no demonstrated predictive advantage over trivial no-op; dependency is constructed, not learned. Next: external independent target and adversarial alias tests with separately preregistered protocol.