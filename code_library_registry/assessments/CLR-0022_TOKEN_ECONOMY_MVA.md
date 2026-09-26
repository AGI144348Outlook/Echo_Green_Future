# CLR-0022 — Token Economy MVA: Capability and Admission Algebra

## Classification
Historical capability/governance prototype. Strong lineage relevance to Echo token permissions, Governor validation, Registry-bounded composition, and Notebook ActionRequests.

## Core contribution
The prototype separates token authority into distinct predicates:
- TC: authority/capability to create a token/symbol;
- TI: authority/capability to issue it;
- TA: authority/capability to admit it;
alongside structural roles:
- container;
- carrier;
- carried.

This is more durable than the UI demonstration. It is an early capability protocol: creation, transport/issuance, and admission are independently governable operations.

## Formal reading
Let capabilities be predicates over actors/objects:
`TC(x), TI(x), TA(x), Container(x), Carrier(x), Carried(x)`.

The implemented admission rule is approximately:
`Admit(r,t) iff TA(r) AND Carried(t)`.

The implemented composition rule is:
`Create(d,C) iff TC(d) AND C subseteq Carrying(d)`.

This gives Echo a bounded-generation principle: a domain may construct only from operands explicitly available in its carried set.

## Important implementation contradiction
createSymbol() returns symbols with:
`C_carried: false`.
But the later demonstration passes symbol1 to admitToken(), which requires:
`token.C_carried === true`.

Therefore Step 7 cannot report successful admission. It returns:
`Token cannot be carried`.

The UI text claims successful token flow, but the executable object schema forbids it. This is valuable because it exposes a missing distinction between a symbol/container and an issued transferable token.

## Recommended type split
Do not overload one object with all roles.

`Pattern` — compositional operand.
`Symbol` — newly constructed semantic/structural object.
`TokenInstance` — transferable capability-bearing reference to a symbol/payload.
`Domain` — bounded namespace/environment carrying admissible patterns.
`Operation` — recipient/action endpoint.
`Capability` — create/issue/admit permissions.
`Provenance` — creator, source operands, issuance chain, admission decision.

Then:
`Symbol = Compose(domain, patterns)`
`TokenInstance = Issue(issuer, symbol)`
`Admit(recipient, token)`.

## "Fresh meaning" claim
The code demonstrates fresh **combinations/identifiers**, not demonstrated semantic meaning. `p1+p2` is mechanically concatenated and labelled "beginning+flow"; no behavioral semantics, grounding, interpretation, or novelty metric is tested.

Use:
- fresh composition;
- novel token instance;
- derived symbol;
until an independent semantic test establishes meaning.

## Generality claim
The invalid p4 example demonstrates membership enforcement against a domain's carried set. It does not by itself establish "generality." Generality would require transfer or abstraction across multiple domains/instances under a shared rule.

## Security/governance limitations
Boolean flags embedded in mutable objects are not secure capabilities. Any code able to mutate an object can set LG_TC/LG_TI/LG_TA. In Echo's governed architecture, permissions should be validated by the Governor/capability registry, scoped to subject/object/action/environment, and accompanied by provenance/audit.

Recommended authorization relation:
`Permit(subject, action, object, environment, constraints)`.

## Architectural synthesis
This prototype can be modernized into:
`Registry operands -> Domain scope -> Compose request -> Governor validates TC + operand membership -> Symbol artifact -> Issue request validates TI -> TokenInstance -> recipient validates TA + schema/capability -> admission trace`.

This maps directly to Notebook typed ActionRequests and the token-as-permission architecture.

## Relation to Hebrew/operator work
The same protocol can govern glyph/operator composition without asserting semantic meaning:
- a Glyphic Registry/domain carries approved operator refs;
- TC permits constructing an ordered operator expression from carried refs;
- TI permits exposing/dispatching that expression as an executable token;
- TA permits a target NVE/operation to accept it;
- Governor verifies domain/codomain and composition constraints.

Thus capability algebra can constrain operator agency independently of what the glyphs mean.

## Status
High-value historical governance ancestor. Correct the symbol/token type contradiction before using as an executable permission model.
