# 90,000-turn language experiment — actual results

Prospective test issue: #111. This is a **negative generalization result**, not language acquisition.

## Setup
10,000 reloads, exactly nine interactions per reload, 27 persistent glyph-named agent IDs; synthetic English-looking noun/relation strings. Same deterministic synthetic target used for training and scoring; 20% of unique ordered (noun, relation, noun) keys withheld by stable SHA256 split; third sentence template held out from training. Each subagent has `origin=Alg-000`, a persistent `self` reference and a version increment per reload. This is **not** operational implementation of the A-000 recursive equation, nor a real language parser.

## Results
- Adaptive: training-known 442/442 (100%); held-out triples 11/86 (12.79%); unseen-template familiar triples 442/442 (100%).
- Non-learning constant-zero control: held-out triples 45/86 (52.33%); unseen-template familiar triples 219/442 (49.55%). Baseline has no train-known examples.
- Both conditions: 90,000 turns, 10,000 reloads, 100,000 event hashes; 27 stable agent IDs; all 27 versions = 10,000.
- 11/11 local unittest controls PASS.

## Caveats
- Adaptive model memorizes observed triple labels and falls back to a weak neighbor-vote heuristic; **held-out generalization is worse than baseline**.
- Template test uses the same structured key, so perfect performance is *not* learned syntax, only surface independence in the code.
- Candidate tokens are accepted by repetition count, not by independently validated compression, accuracy or cost; cannot claim F2-c validated merge.
- Agents carry identity metadata but do not autonomously reason; A-000 recursion remains declarative.
- The supplied neuroplasticity PDF is a proposed candidate menu, not proof of mechanisms.
- Source/tests/results generated and executed in local container, **not committed as exact bytes in this branch**; GitHub replay remains unverified. This report is a verified record of local execution, not a CI receipt.

## Falsified hypothesis
Outcome-history memorization alone would transfer to held-out typed relationships. It did not (11/86).

## Next test design
Teach typed argument roles and relation operators rather than memorizing triples. Use compositional rules with separate training/validation/test partitions; include reversals, negation, new entities and paraphrase structures; evaluate strict no-leakage and ablations. Implement explicit recursive A-000 composition with identity continuity separately. Do not declare language development based on hash uniqueness or template substitution.
