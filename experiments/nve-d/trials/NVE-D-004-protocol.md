# NVE-D-004 reproducibility source
# Complete runnable source available in accompanying downloadable artifact in conversation.
# Experiment protocol:
# 20 seeds (100..119) x 3 synthetic targets; 100 sequential generations per run.
# Population 24, six real-valued weights; each mutation changes one weight by ±0.25.
# Frozen: no mutation.
# Random archive: random mutations of sampled initial candidates, retain best-so-far.
# Selection: top six candidates survive, 18 mutated descendants; retain best-so-far.
# Scoring: mean squared error on 36 deterministic samples plus .002 per nonzero weight.
# Held-out shift: +103 in the input index; fixed per task.
# This is a surrogate experiment, NOT established Mashet glyph semantics.
