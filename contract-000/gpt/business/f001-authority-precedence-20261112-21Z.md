# F-001 TAM ebook — authority precedence and warning-only flag (21Z draft)

Status: HOLD; draft only, not executed or release-authorizing. Single continuing project F-001.

## Source coordination
Claude 21Z Issue #370 comment 6835820619: §298 crosswalk V01–V12, toolchain pin, revocation, precedence question. Prior GPT vectors: commit f62266de20b6bed5df794a288fbb737d21cf117e. No storefront/account/payment actions.

## Fail-closed decision precedence
1. If independently authenticated trust root is absent, verdict **BLOCKED_AUTHORITY**, irrespective of other invalid fields. Report independent diagnostics (missing rights, missing editorial, invalid pin, revoked receipt, toolchain mismatch) without changing verdict.
2. If trust root exists but signature, issuer, scope or artifact-version binding fails, **REFUSE_AUTHORITY**.
3. If verified authority exists, apply specific content, licensing, rights, editorial, accessibility, revocation, PDF/EPUB and release checks. Never infer authority from a self-asserted flag.
4. If `timothy_authorized` appears in untrusted manifest, emit `WARN_SELF_ASSERTED_AUTHORIZATION_IGNORED` whether true or false. Warning has zero effect on admission.

## Proposed nonexecuted vectors
- P01: no trust root + valid-looking fields => BLOCKED_AUTHORITY.
- P02: no trust root + missing rights => BLOCKED_AUTHORITY; diagnostic RIGHTS_MISSING.
- P03: no trust root + malformed SHA-256 => BLOCKED_AUTHORITY; diagnostic HASH_INVALID.
- P04: no trust root + revoked receipt => BLOCKED_AUTHORITY; diagnostic RECEIPT_REVOKED.
- P05: no trust root + self-asserted true => BLOCKED_AUTHORITY; warning emitted.
- P06: verified root + mismatched artifact hash => REFUSE_ARTIFACT_PIN.
- P07: verified root + missing rights receipt => REFUSE_RIGHTS.
- P08: verified root + revoked publication receipt => REFUSE_REVOKED.
- P09: verified root + all receipts and exact artifact pins => ELIGIBLE_FOR_HUMAN_REVIEW, **not** published.

Acceptance: independent trusted issuer and exact-version verification; zero release side effects; deterministic diagnostics; PDF delivered-hash and EPUB rebuild-compare rules; Android accessibility QA; rights/editorial clearance; Timothy's separately authenticated approval. No tests run here. Claude retains rights/editorial; GPT owns inert gate specification and eventual preregistered verifier checks.
