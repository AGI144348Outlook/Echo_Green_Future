# ECHO Classroom benchmark sources

Purpose: provenance for external benchmark projects selected for the ECHO Classroom. Gold answers stay hidden from ECHO until its response is recorded; only then are they revealed for grading and later Mirror feedback.

## BLiMP
Repository: https://github.com/alexwarstadt/blimp
License: CC-BY (upstream README).
Use: 67 grammar sub-datasets of minimal pairs, with linguistic-phenomenon metadata. We use it for controlled grammatical-structure tests and phenomenon-level scores.

## Zorro
Repository: https://github.com/phueb/Zorro
License: MIT (upstream repository).
Use: minimal-pair grammar tests with vocabulary selected partly from child-directed language. Upstream encodes ungrammatical sentences on odd lines and grammatical sentences on even lines. This is useful as a developmental bridge from ECHO's small-vocabulary experiments.

## BoolQ
Repository: https://github.com/google-research-datasets/boolean-questions
License: CC BY-SA 3.0 (upstream README).
Use: passage + natural yes/no question + gold Boolean answer for reading comprehension. We use labeled examples while withholding the answer during administration. Upstream is archived/read-only as of 2026.

## DREAM
Repository: https://github.com/nlpdata/dream
Terms: non-commercial research purpose only (upstream license.txt).
Use: dialogue-based multiple-choice comprehension, useful after BoolQ for contextual inference and later communication-oriented tests. Do not vendor or redistribute DREAM data in ECHO; respect its non-commercial restriction.

## Import policy
Do not copy whole upstream repositories into ECHO. Keep adapters and provenance here; fetch/pin benchmark data separately. This keeps answer isolation auditable, avoids repository bloat, and preserves upstream attribution.

## Classroom boundary
1. Construct an item containing prompt and sealed gold answer.
2. ECHO receives only the public test view.
3. Record ECHO's response before revealing the answer.
4. Grade and reveal the gold answer.
5. Permit Mirror feedback only after grading.
6. Measure transfer on previously unseen items.

Mirror-mediated improvement is an experimental hypothesis to measure, not an assumed equivalent of reinforcement learning.
