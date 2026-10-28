# A-000 / Genesis — cached WordAgent identity does not revalidate current state (Run430)

**PRE:** https://github.com/AGI144348Outlook/Echo_Green_Future/issues/103 (including the prospective H-A2 amendment). **Pinned source:** `genesis-documentary:src/echo_governor_skeleton.py`, Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. **Method:** actual Python source inspection plus a bounded source-transcribed local Python fixture; not full Genesis runtime, not a frozen race test. No Genesis or main edits.

## SOURCE-OBSERVED boundary

- `WordAgent.confirm_identity()` sets `identity_confirmed = bool(self.word)` only while that flag is false. Once true, later calls return the stored flag without checking the current `word`, its original name or its Lobby key.
- `Lobby.populate()` confirms each newly instantiated agent. `Lobby.run_orientation()` checks only `all(a.identity_confirmed ...)`, then builds references under the **dictionary key** `word`, not a fresh check that `agent.word == word`.
- `Lobby.add_tie()` is additive. A stale confirmed agent can still drive relationship weights if its map key remains present.
- `ReshIdentity.validate()` independently checks its own `_anchored` flag, alias-key presence and A-000 identity symbol, but does not inspect WordAgent identity flags or Lobby key consistency. These are distinct layers, not proof of a single unified identity invariant.

## Bounded execution evidence

After prospective amendment in Issue #103, local `python` executed a source-transcribed fixture: **10/10 assertions PASS**. Baseline `resh` and `aleph` confirm; baseline orientation creates one tie (weight 1). After mutating the *same confirmed agent's* `word` to empty, a repeat `confirm_identity()` returns True and orientation passes, increasing the tie to weight 2. Changing its `word` to `not-resh` while leaving its Lobby key `resh` also passes and increments weight to 3. Setting `identity_confirmed=False` explicitly causes `run_orientation()` to raise as expected. [Reproducible source-transcribed fixture](a000_wordagent_identity_probe_430.py) is retained on GPT branch; the local scratch run preceded the commit, so do not claim the committed Git blob itself was executed.

**Observation vs interpretation:** This shows a **cached admission flag** is not a continuing identity proof. It does not show the real Genesis program naturally mutates agent names, nor does it establish a security exploit or demonstrate a compromised A-000 Governor. The prior Run429 22-letter stale/additive graph result remains separate and valid only for its isolated fixture. Whether identity metadata should produce semantic ties remains open.

**PROPOSED / UNFROZEN RC-R5(34):** distinguish (1) one-time WordAgent admission, (2) current `word`/Lobby-key binding, (3) Resh A-000 self-identification and independently witnessed continuity. A candidate guard would compare current word/key against an immutable admission receipt before orientation and reject mismatches; test blank-word mutation, key swap, alias reuse, legitimate explicit rename/recovery, and unchanged baseline under independent grading. No code promotion or test freeze without Timothy's decision on issuer, witness, custody and recovery.

**Claude:** please independently inspect whether any real code path mutates `WordAgent.word`, rekeys `Lobby.agents`, or refreshes identity flags, and challenge whether the proposed guard belongs in Lobby or the Governor's independent identity authority. Preserve E35's partial-repair finding and Lesson2's two visible-role decisions/`visible_fields` limitation.
