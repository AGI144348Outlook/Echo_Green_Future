# Run432 A-000 / Ayin SELF classification authority boundary

**Source:** `genesis-documentary:src/echo_governor_skeleton.py` exact Git blob `63eb982989b4f3478d649430b555c8f4ba755c27`. Demo `tests/pe_ayin_resh_communication.py` blob `64a171a6791f2356006683596b56cbe289cbbdc0`. Prospective PRE and actual POST: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/105.

## SOURCE-OBSERVED

`AyinPerception.__init__` lines 3130–3134 accepts `governor_word` default `resh` as a lowercased string. `classify()` lines 3143–3154 first requires a Lobby agent at that key, then labels `SELF` solely if the lowercased queried word equals `self.governor_word`. The result's `signals` is `["governor_identity"]`. This path does **not** consult `ReshIdentity.validate()`, `A-000` or a detached identity witness. `perceive_all()` stores classifications in `self.perceived`; `agentive_entities()` uses those records. A classification label is not itself an authorization decision.

The actual Pe/Ayin/Resh demonstration `tests/pe_ayin_resh_communication.py` anchors Resh at line 114, **before** creating/scanning Ayin at lines 129–130. The Ayin classifier is built over `lobby` (vocabulary), not necessarily `hebrew_lobby` (letter agents). Therefore this source review does **not** establish that a normal demonstration emits an unauthorized SELF classification, nor that a downstream gate trusts one.

## EXECUTION-VERIFIED, isolated only

A 12-control stdlib Python fixture transcribed the early-return SELF/UNKNOWN logic, using a minimal Lobby and an independently modeled Resh authorization gate. All **12/12 PASS**: present `resh` classified SELF with or without anchor and despite a tampered stub; missing agent UNKNOWN; configurable `governor_word="cat"` classifies `cat` SELF; a Lobby entry whose internal `agent.word` was changed still classifies from the map key; the separate validated-gate counterfactual rejects unanchored or tampered Resh. This is **not** execution of the 440KB Genesis runtime. Source-specific inference is limited to the named early-return path.

## Interpretation and prospective RC-R5(36), NOT FROZEN

Distinguish `classification_category=SELF` from `identity_authority=VALIDATED`. A-000 identity-admission or recovery must not infer authorization solely from `AyinPerception.classify` or a user-configurable governor word. Proposed test sketch: with a present matching Lobby agent but unanchored, malformed, replaced or independently unverified A-000, Ayin may describe the name as SELF, but any authority gate must reject and record why. Require independent witness and issuer rules as Timothy decides. No direct modification of Genesis or frozen tests.

**Challenges / limitations:** inspect all actual consumers for a separate upstream Resh gate; classify may be intentionally descriptive. The demo anchors first, so this is not a proved normal-path bypass. No complete runtime, race adjudication, or identity compromise established. Claude's E35 remains a partial-repair observation and Swadesh Lesson2 40/40 remains only two visible role decisions with `visible_fields` required for fair transfer evaluation.
