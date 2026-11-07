# GPT spatial oracle 18Z — results and limitations
Preregistered **before execution** in Issue #336; committed Python source ba044eb34631d4b479c61e39585cf294ceafdf0f (blob 2727a662b86bcfb33959413ed063b34bc61e022f). Fetched exact source from GitHub. Attempt to download raw committed source into container failed DNS, so code was manually reproduced and run with Python. This is **not** byte-for-byte execution of the downloaded committed file; further independent exact-blob replay remains outstanding.

Four fixed seeds 1109,2203,3301,4409; ten distinct test categories; 40/40 implemented checks true, zero false. Candidate loss vs no-op loss against separately specified target diffusion coefficient 0.21 (candidate 0.15):
- 1109: 0.00093613 vs 0.01146764
- 2203: 0.00136058 vs 0.01666709
- 3301: 0.00054384 vs 0.00666206
- 4409: 0.00038434 vs 0.00470822

Tests: unique 27 coordinates; six center neighbors; no-op; zero coupling; one-step locality; two-step distance-two spread; deterministic replay; shuffled label structural invariance; negative-coupling neighbor sign; independent-target loss comparison. Observations are synthetic. The target uses the same model family as the candidate with coefficient chosen near candidate, so improvement is expected by construction. This repairs the literal target=self tautology of #335 but does NOT demonstrate generalization, learning, or semantic benefit. No real multiring phase/frequency or deformable boundaries. After-test narrative posted to same Issue #336 comment 6711056585. Next: independently sourced held-out dynamics and negative/null competing models, with prospective preregistration.