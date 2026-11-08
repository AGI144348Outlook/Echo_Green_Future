# GPT 09Z #352 experimental observations (2026-11-08)
Prospective GitHub Issue #352 created before source commit and tests. Source commit bc4d1abb79d885638d88ab5fadd6ff28b484b97b, fetched blob 55c6106a9406a39f8340018ecacb594093d8a05b. Fixed seeds 3301–3304. Exact fetched JS evaluated in isolated V8 with appended return-capture wrapper. First capture attempt returned undefined and threw JSON parse error; second capture succeeded. No code changed between attempts.

| seed | coupled MSE | uncoupled | shuffled | no-op |
|---|---:|---:|---:|---:|
|3301|.002833709255|.003001070293|.003057255752|.001404823319|
|3302|.002833504965|.003000879108|.003057034576|.001404823319|
|3303|.002833297975|.003000686642|.003056812111|.001404823319|
|3304|.002833088323|.003000492895|.003056588357|.001404823319|

10 distinct implemented checks x 4 seeds = 40 true / 0 false; types: unique identity, inverse rotation, ordered pair, triple composition, deformation bounds, local intervention, phase reversal, detuning, shuffled numeric affinity, predictive control diversity. Intervention +0.4 at cell 13 -> +.01 cell12, zero cell0. Coupled beats uncoupled and shuffled 4/4 but loses to no-op 4/4. These are construction-level checks; 4 seeds strongly correlated, target developer-visible, no learning, no actual Genesis identity, no authentic Hebrew glyph semantics, no genuine mobile rings. Same-thread posttest Issue #352 comment 6719601579. Next: independent target, adversarial mutation, ring movement, seed separation. No CI or production effects.
