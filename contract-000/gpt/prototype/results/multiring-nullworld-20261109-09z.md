# GPT 09Z multiring independently generated null-world results
**Prospective:** Issue #367 comment 6736829907 before source commit. **Source:** fef69f256b3802a919bc45c6e58e7b5a0cba99c7, blob 173a5c30c6f8f3dc024d21e26ae4d36e6129cc88. **Execution:** GitHub connector exact-source retrieval then isolated V8 evaluation, no CI, no paid inference, four fixed seeds 4401–4404; 120 training and 120 held-out points per world. **Post-test:** Issue #367 comment 6736838538.

| Seed | Signal linear MSE | Signal quadratic MSE | Signal zero MSE | Null quadratic MSE | Null zero MSE |
|---|---:|---:|---:|---:|---:|
| 4401 | .318261 | .161368 | .412570 | .181745 | .181552 |
| 4402 | .330679 | .167912 | .412523 | .181762 | .181583 |
| 4403 | .307683 | .172507 | .453754 | .181036 | .180995 |
| 4404 | .302369 | .167799 | .445121 | .180110 | .180072 |

40/40 scripted construction/finite checks pass; signal quadratic beats linear 4/4; null quadratic beats zero 0/4. No independent causal interpretation follows. Null target uses a deterministic sinusoid unrelated to x,z, and only one null family; source also prints uncoupled, shuffled, phase-reversed and detuned MSE for each seed. Ten test *types* include structural checks; do not interpret as ten independent predictive achievements. No actual semantic/gematria-learning mechanism or adaptive boundary dynamics yet. Next: multiple null generators, leakage checks, time-respecting CV and uncertainty estimates.
