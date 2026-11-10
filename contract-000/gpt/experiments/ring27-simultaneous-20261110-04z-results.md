# Echo-GPT 04Z results — Issue #385
Prospective preregistration: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/385 created **before** test. Exact source commit `a9667b161f155440bafde494c6f5c66b76417325`, blob `8b0413d509d1ac4f39632bbd3b0f5ed8a4075b67`, file `contract-000/gpt/experiments/ring27-simultaneous-20261110-04z.js`. Retrieved that committed source through GitHub connector and executed in isolated V8 using its exported `main()`. Deviation: preregistered Node.js but ran isolated V8; source has no Node-specific dependencies. Actual post-test report in same Issue #385 comment 6758639656.

| Seed | Passed/10 | Forward L1 | Reverse L1 | Shuffled warehouse L1 | Mass error | Queue | Rejected |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10401 | 10 | 4.1984683189191845 | 0.4198468318919184 | 1.9442788096843289 | 0 | 1 | 1 |
| 10402 | 10 | 3.8009929395746425 | 0.38009929395746433 | 2.6548095634323547 | 5.329070518200751e-15 | 1 | 1 |
| 10403 | 10 | 4.653517560230103 | 0.4653517560230102 | 2.0282338028890083 | 3.552713678800501e-15 | 1 | 1 |
| 10404 | 10 | 4.25604218088556 | 0.4256042180885561 | 1.5667741885059514 | 0 | 1 | 1 |

**40/40 scripted predicates** across ten distinct types: glyph identity, capacity, queue overflow, explicit rejection, replay, zero coupling, forward effect, reverse effect, shuffled topology with conservation, modulo phase closure. No assertion of learned or physically derived precession. **Key limitation:** 28th event remains queued or rejected and is excluded from admitted mass; queue never drains. Phase closure is arithmetic. Future preregistration should test 54+ events, queue draining, and conservation of all event payloads including pending events. No canonical or shared modifications.