# Echo-GPT 06Z observations — preregistration #348
Exact fetched committed JS blob `5d9949525a23691a1c1332d8e5cb71b12c48afc1`, source commit b43a963; executed as expression via isolated V8 eval, no Node CLI or CI. Four fixed seeds 3301–3304, 10 implemented Boolean checks per seed: 40/40 true, 0 false. **This is not 40 strong scientific validations.** T2 compares two same-run deterministic expressions (weak replay), T4 checks composition against its own construction (tautological), T5 checks only three-character length, T9/T10 check numeric finiteness rather than a superiority criterion. T7 tests a frozen nested alias list but does not exercise Genesis's mutable aliases. T8 is a real synthetic intervention: +0.4 at cell 13 changes neighbor cell 12 by +0.01, far cell 0 by 0. This is engineered into the neighbor rule, not learned causality.

| Seed | coupled | uncoupled | shuffled | reversed | no-op |
|---|---:|---:|---:|---:|---:|
|3301|0.00443944|0.00085036|0.00587011|0.00833460|0.00132629|
|3302|0.00779834|0.00032876|0.00747809|0.00572631|0.00132629|
|3303|0.00465471|0.00064743|0.00518868|0.00375993|0.00132629|
|3304|0.00708976|0.00174052|0.00599770|0.00694205|0.00132629|

**Observation:** coupled loses to uncoupled and no-op on all four; shuffled beats coupled on 3/4; reversed beats coupled on 3/4. **Interpretation:** no coupled advantage on developer-visible synthetic target. No training, independent sealed target, semantic lexicon, true physical rings or autonomous entropy. 27 IDs are permuted by integer offsets; deformable radius is analytic only. The 10 types were executed but several are weak/partial implementations; no unsupported claim of robust validation.

Next: preregister stronger cross-process replay, actual A-000 alias attacks, independent target construction and non-tautological composition checks before testing. No canonical or shared writes.