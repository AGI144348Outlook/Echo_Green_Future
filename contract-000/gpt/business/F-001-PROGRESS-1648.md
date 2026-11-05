# F-001 TAM Protocol ebook — GPT 16:48Z packaging/custody development

Single continuing income project F-001, not a new pipeline. Read shared decision sheet blob 2975edcc4cae8a17499e873b68ba75f5c39ea527 and prior GPT 16Z progress. Claude independently handles editorial, rights and listing; GPT handles source pin, custody, packaging verification. Status HOLD / NOT LAUNCH-READY.

## New technical deliverable: bounded verifier change contract (source review only, no tests)

Draft patch requirements for 15Z H3c verifier, blob db8131dffa4cbc040bc9f23a5755fb2b31c3325f:
1. Enforce MAX_SOURCE_BYTES=16*1024*1024 and MAX_TOTAL_BYTES=64*1024*1024, MAX_ENTRIES=128 as *provisional test policy*, not canon. Check fstat size before opening the read loop, then cumulative byte counts after each chunk; refuse oversize with HOLD. Bound JSON manifest bytes before parsing.
2. Reject path traversal, absolute paths, NUL, symlink and casefold-colliding names; accept a legitimate spaced extensionless filename. Preserve directory-fd no-follow behavior where supported; unsupported platform HOLD.
3. Require independently pinned Git tree/blob identifiers; never treat caller-provided source_commit or manifest approvals as authoritative. Before/after fstat does not prevent same-inode concurrent mutation; prefer immutable Git blobs or a trusted snapshot.
4. Separate read and close failures in evidence receipts; any close error is HOLD. Never convert synthetic booleans into owner authorization.
5. Keep release state HOLD until source provenance, editorial rights receipts, accessibility/PDF/EPUB checks and explicit Timothy authorization are independently verified.

**Checklist:** [x] technical threat review; [x] bounded patch design; [ ] implement source-bounded verifier; [ ] preregister adversarial test family; [ ] execute exact-source adversarial tests and commit outputs; [ ] source-pinned reproducible PDF/EPUB; [ ] accessibility and Android review; [ ] Claude editorial and rights signoff; [ ] Timothy A1–A6 and explicit publication approval.

**Acceptance:** fail-closed for altered bytes, oversize, symlinks, traversal, collisions, close error, spoofed approvals, stale pin and mutation; safe extensionless path accepted; evidence reproducible. **Next GPT action:** implement bounded patch and preregister F-001-specific tests before execution. No publishing, outreach, accounts, payments or spending.