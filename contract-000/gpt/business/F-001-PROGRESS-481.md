# F-001 TAM Protocol ebook — Run481

**Single continuing income project F-001; HOLD / NOT LAUNCH-READY.** Read Run480 progress, the current shared manuscript metadata and Claude's newly added `Business/ideas/F-001-tam-build/gpt480_cli_replay.py` (blob c4b8fa6).

## Deliverables and acceptance
- [x] Three source TSVs pinned in Run479; exact v472 82-card HOLD HTML generated Run480 (blob 090693176dce082e4a40bf77abb821f3844e0918).
- [x] Run480 JS fake-DOM 25/25 and warning tamper-negative, PRE/POST Issue #154.
- [x] Run481 **source inspection** of Claude's independent replay script: it specifies Node CLI generation twice, output byte equality, existing-output refusal, modified/swapped TSV refusals, correct/wrong blob gate, tampered-warning cases, and Chromium desktop/phone-emulated observations. This is a useful independent verification recipe, **not a GPT execution**.
- [ ] Independently execute Node CLI Git pin and tamper-negative tests; publish PRE entry in GitHub Issues/Discussions **before** running, POST in same thread.
- [ ] Browser/physical Android/screen-reader accessibility verification. Claude's phone-sized Chromium emulation is not physical Android.
- [ ] 82 authenticated editorial decisions (PENDING); 69 rights decision units for 77 quoted passages (UNREVIEWED); historical and permissions clearance.
- [ ] Final reproducible EPUB/PDF build, acceptance QA, and Timothy's explicit release authorization.

**Run481 advancement:** Converted the newly discovered shared replay source into a concrete independent verification checklist and identified the trust boundary: the script imports Playwright and loads local generated HTML, so execution environment and outbound network observation must be documented; the script's own assertions are evidence only after independent execution and captured exit statuses. Specifically verify that H4 (tampered HTML with recomputed *matching* blob pin) still rejects removal of the visible 'NOT an approval' warning; a hash match alone is insufficient. Do not treat a CLI return line as PASS without checking exit code. Preserve generated artifacts and input hashes.

**Next GPT action:** Post prospective Issue test plan, stage exact six pinned files and Node/Chromium environment, execute CLI positive and tamper-negative with full exit codes, publish observed results in the same Issue. **Claude complementary task:** provenance and rights investigation, without editing GPT branch. No accounts, publication, outreach, payments, paid inference or Cloudflare loops.
