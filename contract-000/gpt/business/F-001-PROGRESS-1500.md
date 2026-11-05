# F-001 TAM Protocol ebook — GPT 15Z continuation
Project ID F-001 only. Prior GPT progress: `contract-000/gpt/business/F-001-PROGRESS-1400.md` blob `09d65864b98307fdd20f7c42e4dc79392ffc588c`. Shared Claude source `Business/ideas/F-001-tam-build/CLAUDE-h3c-source-files-189.py` blob `d71fe650dc2d105f4d268229c6da1fda32b5a7b0`, shared decision sheet blob `2975edcc4cae8a17499e873b68ba75f5c39ea527`.

## Concrete increment
Added `f001_h3c_custody_draft_1500.py` on GPT-only branch. Draft uses directory-relative file descriptors with O_NOFOLLOW, rejects traversal/duplicates/symlinks/nonregular inputs, compares fstat before/after, checks pinned SHA-256/size/source commit, and refuses missing editorial, rights and release approvals. It intentionally **always returns HOLD**, even for internally consistent inputs, because independent custody authenticity is not established. This is untested draft code; no F-001 tests were run, and no packaging validation or release was performed. It is not a replacement for Claude's pin converter or independent receipt.

## Acceptance / ownership
[ ] Pre-register and execute adversarial source verifier tests (symlink, traversal, mutation, close/error, missing approvals, corrupted digest).
[ ] Independent custody witness/receipt verification and source pinning.
[ ] Reproducible PDF+EPUB, integrity and accessibility/Android review.
[ ] Claude editorial and quotation-rights dispositions; historical review.
[ ] Timothy A1–A6 decisions, explicit release authorization.
Next GPT action: preregister adversarial verifier tests and inspect any failures; integrate Claude's pin converter without overwriting his file. Claude retains editorial/rights/listing. Status HOLD / NOT LAUNCH-READY. No publication, account creation, outreach, payment, or spending.
