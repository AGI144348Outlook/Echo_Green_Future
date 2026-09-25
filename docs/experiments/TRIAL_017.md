# Trial 017 — Existing Tool Discrimination

Trial 016 localized the bottleneck to proposal generation. Before changing ECHO, Trial 017 asks whether an already-implemented ECHO learning mechanism (A-102 TF-IDF similarity) contains enough signal to discriminate among the Hebrew/Mashet tool descriptions for the same goal.

This is diagnostic, not agency and not execution. The harness does not encode a preferred glyph/operator or expected winner. It indexes the goal and every tool description, then invokes the existing AlgorithmMatrix TF-IDF similarity method. A positive result only means ECHO's existing substrate can produce differentiated relevance measurements that a future Propose implementation could consume.
