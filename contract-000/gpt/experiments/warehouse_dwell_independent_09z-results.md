# GPT 09Z experiment results — Issue #321 (POST-TEST)

Pre-test issue: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/321 — published before source execution. Committed prototype `contract-000/gpt/experiments/warehouse_dwell_independent_09z.py` @ `bb94cffdff198c30fbe101fa72d4e904de189d48`. **Execution used a local transcription**, not fetched exact bytes; container DNS to GitHub raw was unavailable. Local command: `python /mnt/data/warehouse_09z_local.py` (Python stdlib). Fixed seed 1106; 270 opportunities; dwell 3; seven views; 27 seats. Local transcription's first redundant phase-initialization statement is immediately overwritten by the correct seeded seven-draw initialization; not byte-identical to GitHub source.

|Check|Observation|
|--|--|
|01 same-glyph new seat blocked|TRUE|
|02 new-glyph occupied seat blocked|TRUE|
|03 out-of-range blocked|TRUE|
|04 absent leave no-op|TRUE|
|05 dwell projection persists until expiry and clears|TRUE|
|06 26/27 actual entries: intermediate phase and closure|TRUE|
|07 zero entropy no entries|TRUE|
|08 high synthetic entropy > low|TRUE|
|09 reverse intervention changes trace without changing tick count|**FALSE** (trace changes, 103 vs 129)|
|10 forward/bidirectional feedback changes trace without tick count change|**FALSE** (both 125 vs forward 129)|

Observed accepted ticks: zero 0, low 20, high 225, none 129, forward 129, reverse 103, both 125, shuffled 112. Bidirectional phase 226.66666666666669 degrees; deterministic replay true. **8/10** checked hypotheses true, not ten passed. The two failed stronger hypotheses are informative: seat-selection changes can affect collision and accepted occupation rate during dwell. Entropy gates *attempts* but does not alone set *successful ticks* in this implementation. No predictive task, measured Neon entropy, source injection, or real learning. Next: explicit opportunities/attempts/accepts/rejections, queue-vs-drop controls, multi-seed and exact-byte reproduction. No canonical modifications.
