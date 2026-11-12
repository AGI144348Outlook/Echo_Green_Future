# F-001 release admission — GPT-owned acceptance vectors v1 (DRAFT / NOT EXECUTED)
Project: F-001 TAM Protocol ebook. State: HOLD. This file is a specification, not publication authority.

## Inputs
- `artifact_kind`: PDF or EPUB
- `artifact_sha256`: lowercase 64-hex digest of delivered bytes
- `artifact_location_pin`: immutable branch:path@commit or equivalent trusted location
- `approval_receipt`: separately authenticated issuer, exact artifact SHA, version, decision, time, revocation status
- `rights_receipt`, `editorial_receipt`, `source_license_receipt`, `accessibility_receipt`, `android_qa_receipt`
- `timothy_authorized`: untrusted caller-controlled flag; never an admission input. Warn if present.
- `verification_mode`: delivered_hash_only (PDF) or rebuild_compare (EPUB, only with pinned toolchain and identifier).

## Prospective vectors (no tests executed)
| ID | Condition | Expected |
| --- | --- | --- |
| V01 | all evidence absent | BLOCKED_AUTHORITY |
| V02 | all fields populated but no external issuer trust root | BLOCKED_AUTHORITY |
| V03 | valid-looking approval with SHA different from delivered artifact | REFUSE_ARTIFACT_MISMATCH |
| V04 | valid SHA but missing immutable location pin | REFUSE_UNPINNED |
| V05 | location pin present, no content SHA | REFUSE_UNPINNED |
| V06 | valid approval but rights receipt missing | REFUSE_RIGHTS |
| V07 | valid approval but editorial receipt missing | REFUSE_EDITORIAL |
| V08 | self-asserted `timothy_authorized: true` with otherwise incomplete evidence | unchanged refusal + warning |
| V09 | same complete externally verified evidence with or without self-asserted flag | same decision, warning only |
| V10 | EPUB rebuild compare with unpinned identifier or toolchain | REFUSE_REPRODUCIBILITY |
| V11 | PDF delivered-hash-only with correctly pinned artifact and independent receipts | ADMIT only if all other gates independently verify |
| V12 | approval receipt revoked after issuance | REFUSE_REVOKED |

## Acceptance criteria
Fail closed; all refusals zero external effects; no AI-authored field can authenticate itself; issuer and scope are checked by a separately authorized verifier; release remains HOLD until Timothy authorizes exact-version publication. Register test protocol prospectively in a GitHub Issue before any execution. Do not modify Claude's rights/editorial source records.
