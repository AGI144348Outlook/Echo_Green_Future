# F-001 — same sole TAM Protocol ebook, Run473

**Project identifier:** F-001. **HOLD / NOT LAUNCH-READY.** Read existing F-001 decision sheet and Run470 progress, Run472 checkpoint, Claude §169 and §170 evidence. Alternate B/C pipelines DEFER.

## New evidence and development

Claude's independently executed §169 Chromium/Node replay of v470 shows 82 cards, 164/164 label clicks focusing controls, successful export/import, no network requests and no page errors on desktop and emulated phone. Claude's §170 scratch variant replaces two `aria-label` overrides with `aria-describedby` pointing to each card heading; the Chromium AX tree then includes the visible **NOT an approval** warning in **82/82** disposition names, compared with **0/82** in the original. The occurrence identifier remains in name or description for 164 controls. These are Claude's measurements on a scratch variant, **not** a GPT-executed test or an independently verified v472 build. Run472 generator candidate is unverified in Node/Chromium.

**Design decision (draft only):** preserve the visible label as the primary accessible name and attach the occurrence heading as description; ensure description references are valid and do not replace the label. The generator v472 already attempts this, but do not claim it works until independently replayed. Avoid further speculative versions until Claude's v472 Node/Chromium replay or a reproducible local test establishes the outcome.

## Checklist / acceptance

- [x] 82 source locations and draft review cards, with source pins and custody evidence; all 82 editorial decisions **PENDING**, no authenticated approval.
- [x] Claude v470 Node/Chromium replay §169, and Claude scratch variant AX experiment §170 (limited scope).
- [ ] **Next action:** independently run v472 pinned Node CLI, no-clobber and tamper negatives; inspect computed Chromium accessible names and descriptions, keyboard navigation, draft restore; publish a prospective issue plan before any tests and actual POST in same thread. Physical Android and screen reader remain unverified.
- [ ] Timothy's authenticated editorial approvals, rights and historical claim clearance, final EPUB/PDF reader checks, listing, pricing, and explicit release authorization.

No new tests or CI triggered in Run473. No publication, account creation, outreach, spending, payments, paid inference or Cloudflare loop.
