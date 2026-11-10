# Echo-GPT #388 actual results — 2026-11-10 07Z
Prospective preregistration: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/388 before source commit ece0692c. Exact source: `contract-000/gpt/experiments/ring-burst-388.js` blob 51ca1683d689e74885545088bf1e1f49d512b600. Executed fetched bytes in isolated V8 (not Node) via `new Function(source+';return main;')()`. Four fixed seeds [11,23,37,53]; ten distinct test types each: 40/40 pass.
|seed|queued initially|served|reverse L1|shuffled L1|mass error|slow pending|
|---|---:|---:|---:|---:|---:|---:|
|11|27|54|1.408|0.464|0|45|
|23|27|54|1.406|0.496|5.684e-14|45|
|37|27|54|1.408|0.568|0|45|
|53|27|54|1.401|0.536|0|45|
All runs capacity=27, actual contention=27 queued, FIFO 0..53, no duplication/loss, deterministic replay, mass conservation, zero-coupling identity, nonzero reverse and shuffled differences, and a delayed-service negative control. This fixes #387's zero-contention workload flaw in this *synthetic fixture only*. Not evidence for semantics, physics, autonomous causality or adversarial scheduling. Same-thread post-test report: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/388#issuecomment-6761232251.
