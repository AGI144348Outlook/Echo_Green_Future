# ECHO Constrained Multimodal Homework Protocol

## Purpose

This protocol defines ECHO's preparation period before independent Classroom
evaluation. Homework may expand ECHO's vocabulary and visual experience, but
must not expose Classroom questions, answer keys, or held-out examination
images.

The experiment is intended to distinguish prior exposure, bounded study,
Mirror-mediated correction, and transfer to unseen material.

## Core permission law

**Lobby membership is permission to study.**

A word must already be instantiated in ECHO's Lobby before ECHO may request:

- its lexical definition;
- its semantic relations;
- its WordNet/synset association;
- its permitted visual examples; or
- a live visual search for that word.

A word encountered inside a permitted definition does **not** automatically
become a Lobby member. It enters a candidate frontier. A bounded later choice
may instantiate it.

This creates the study path:

    Lobby concept
        -> permitted definition
        -> unfamiliar candidate concepts
        -> bounded selection
        -> Lobby expansion
        -> newly permitted definitions / visual examples

## Initial Lobby

The intended experimental starting condition is a small basic-child/basic
vocabulary rather than a completed dictionary.

The exact seed list, source, and hash should be recorded before a canonical
homework run. Existing expanded vocabulary experiments are historical evidence,
not permission to preload the future examination vocabulary.

## Homework Governor

Implementation: `src/echo_homework.py`

The governor maintains:

- Lobby membership;
- candidate concepts discovered during permitted study;
- vocabulary lineage;
- a finite study-turn budget; and
- a maximum number of new words admitted during one instantiation action.

The governor, rather than the lexical or visual provider, owns permission.

## GF WordNet lexical channel

Implementation: `src/echo_gf_wordnet.py`

GF WordNet is used as the lexical/semantic homework channel. The adapter can
associate a permitted Lobby concept with a definition, semantic relations,
WordNet/synset identity, and available image references.

The adapter cannot independently expand the Lobby. Unknown words exposed by a
definition are handed back to the Homework Governor as candidates.

Upstream project:

https://github.com/GrammaticalFramework/gf-wordnet

GF WordNet is connected to Princeton WordNet/Wikidata resources. Upstream
licenses and notices must remain authoritative for imported upstream material.

## ImageNet visual channel

Implementation: `src/echo_imagenet.py`

ImageNet provides multiple visual examples organized around WordNet concepts.
ECHO must possess Lobby permission for the associated word before requesting
examples.

The repository does not vendor ImageNet photographs. The adapter accepts
external references supplied through authorized access and retains hashes in
its exposure audit rather than image bytes or image URLs.

ImageNet:

https://www.image-net.org/

ImageNet states that it does not own the copyright in the underlying images.
Use of ImageNet resources must therefore follow ImageNet access terms and any
applicable rights attached to the underlying material.

## Live visual-search channel

Implementation: `src/echo_live_image_search.py`

Live image search is an optional environmental-variation channel.

It is intentionally implemented as a provider boundary rather than a web
scraper. A future authorized search provider may supply temporary results.
The same Lobby permission law applies.

The adapter:

- rejects searches for concepts outside the Lobby;
- limits the number of results;
- returns results for the active study operation;
- does not archive image bytes; and
- stores hashes rather than raw result references in its audit.

No Google Images scraping mechanism is included.

## Lineage and audit

Implementation: `src/echo_homework_audit.py`

The audit distinguishes events such as:

- seed instantiation;
- definition study;
- definition-discovered vocabulary;
- later vocabulary instantiation; and
- visual exposure.

The audit can be frozen before examination and assigned a SHA-256 fingerprint.

A conceptual lineage may therefore look like:

    seed: water
        -> definition exposure
            -> candidate: liquid
                -> instantiated: liquid
                    -> definition exposure
                        -> candidate: substance

The record is evidence of what ECHO was permitted to encounter. It must not be
interpreted by itself as evidence that ECHO understood or generalized the
material.

## Homework / Classroom separation

The Classroom implementation remains separate from Homework.

Before an examination:

1. finish the allowed Homework period;
2. freeze the Homework Governor state;
3. freeze and hash the Homework Audit;
4. freeze the examination item set;
5. verify that examination questions/answers were unavailable during Homework;
6. verify that held-out visual examination examples were unavailable during
   Homework; and
7. record the relevant source-code commit SHA.

The first examination response must be committed before corrective evidence is
shown.

## Mirror feedback

Mirror feedback belongs after an attempted examination item, not inside the
sealed answer path.

The intended sequence is:

    unseen item
        -> ECHO response
        -> response commitment
        -> reveal permitted evidence / answer
        -> Mirror reflection
        -> structural adjustment
        -> different unseen item

Improvement on later unseen items is the measurement target. It is not assumed
in advance.

## Visual evaluation

Homework images and examination images must be disjoint.

Useful held-out tasks include:

- unseen image -> identify/select a Lobby concept;
- word -> select matching unseen images;
- definition-only versus image-only grounding comparisons; and
- later image-to-language communication.

Multiple visual examples are used during Homework to reduce dependence on a
single memorized photograph.

## Communication evaluation

Communication is a later, separate evaluation axis.

One entity receives information that a second isolated listener cannot access.
ECHO must communicate enough information for the listener to infer or act
correctly. The listener's success, rather than prose quality, is the primary
score.

## Provenance and external sources

Primary project references:

- GF WordNet: https://github.com/GrammaticalFramework/gf-wordnet
- Princeton WordNet: https://wordnet.princeton.edu/
- Princeton WordNet license: https://wordnet.princeton.edu/license-and-commercial-use
- ImageNet: https://www.image-net.org/
- ImageNet access: https://www.image-net.org/download.php

External licenses and terms should be rechecked before a canonical dataset is
downloaded, redistributed, or published. ECHO's repository should prefer
provider adapters, identifiers, hashes, manifests, and reproducible provenance
over redistributing third-party image collections.

## Automated boundary tests

Implementation: `tests/test_echo_homework.py`

The tests are designed to verify that:

- unknown concepts cannot be studied directly;
- definitions create candidates rather than automatic Lobby members;
- admitted vocabulary receives lineage;
- ImageNet access is Lobby-gated;
- live visual search is Lobby-gated and bounded;
- visual audits do not retain raw references; and
- the pre-exam Homework Audit becomes immutable when frozen.

Passing these tests demonstrates enforcement of the specified software
boundaries. It does not by itself demonstrate language understanding, visual
recognition, autonomous agency, or generalization. Those claims require the
subsequent controlled experiments.
