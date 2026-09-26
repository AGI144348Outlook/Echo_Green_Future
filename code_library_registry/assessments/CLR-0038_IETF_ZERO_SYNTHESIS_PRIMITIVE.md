# CLR-0038 — IETF (0,0) Synthesis Primitive

## Classification
Recovered early coordinate-normalization experiment / Reference lineage / Assessed.

## Implementation
Python module:
- simulate random 3D particle positions,
- compute centroid,
- recenter all points by subtracting centroid,
- recursively scale positions down,
- plot the resulting 3D configuration.

## Mathematical reading
compress_to_zero does not collapse all particles to (0,0,0); it translates the cloud so its centroid is at the origin:
x_i' = x_i - mean(x).

recursive_refinement then divides repeatedly by 2,3,...,(iterations+1), giving a total scale factor of 1/(iterations+1)!.

Thus after n iterations:
x_i^(n) = (x_i - mean(x))/(n+1)!.

## Relevance
Useful as an early canonicalization/normalization ancestor: translation-invariant recentering followed by contraction.

It is not by itself a semantic synthesis or proof of information-theoretic compression.

## Status
Assessed / New small historical primitive / Reference.
