# Autonomous Agency — Language Acquisition Research Sources

## Purpose

This note records the language-acquisition and basic-vocabulary sources explicitly referenced during the Claude/ECHO autonomous-agency development work. It separates the historical research from the engineering interpretation applied to ECHO so later experiments can reconstruct why the Lobby was deliberately seeded from a small/basic vocabulary before broader thesaurus expansion.

## Katherine Nelson (1973)

**Source:** Katherine Nelson, *Structure and Strategy in Learning to Talk*, Monographs of the Society for Research in Child Development, Vol. 38, Nos. 1–2 (Serial No. 149), 1973.

Nelson's longitudinal study examined the acquisition of the first 50 produced words of 18 children. The first-50-word analysis reported the following broad distribution used in our design discussion:

- General nominals: 51%
- Action words: 13%
- Modifiers: 9%
- Specific nominals: 14%
- Personal-social: 8%
- Function words: 4%

Examples in the published summary include general nominals such as `ball`, `milk`, `doggie`, `girl`, `he`, and `that`; action items such as `go` and `look`; and modifiers covering attributes, states, locations, and possession.

**ECHO engineering interpretation:** early lexical structure is dominated by concrete/general nominal vocabulary plus a smaller action and relational vocabulary. This was used as evidence against beginning abstraction from a randomly sampled, already-broad thesaurus population.

## Jean Aitchison (1987)

**Source referenced in the development discussion:** Jean Aitchison's 1987 account of vocabulary acquisition, associated with *Words in the Mind*.

The developmental framework referenced during the work was:

1. **Labelling** — associating a word/sound form with something.
2. **Packaging** — learning the range of things to which a label applies, including resolving over- and under-extension.
3. **Network building** — learning relationships among words, including similarities, contrasts, oppositions, and hierarchical lexical relationships.

**ECHO engineering mapping used during development:**

- Labelling → A-115 DictionaryIndexer
- Packaging → A-116 ArticleClassifier / A-117 WordAgent orientation
- Network building → A-119 TypedStudyGroups and thesaurus-network operations
- VGM abstraction → treated by the project as a subsequent engineered abstraction stage, **not** as a fourth stage claimed by Aitchison.

This mapping is an ECHO design analogy, not a claim that the software reproduces human child-language cognition.

## Morris Swadesh — basic vocabulary

**Source family:** Morris Swadesh's basic-vocabulary lists used in lexicostatistics; the commonly called “Swadesh 200” list derives from work including Swadesh's 1952 *Lexico-statistic dating of prehistoric ethnic contacts*. The standard list is commonly represented as approximately 200 concepts (often 207 entries depending on the version).

Swadesh lists deliberately emphasize comparatively basic vocabulary rather than an arbitrary dictionary sample: pronouns, body terms, natural-world concepts, basic actions and properties, spatial/quantity relations, and other common concepts.

**ECHO engineering use:** the Swadesh vocabulary was selected as a principled small seed vocabulary for the Lobby. The intended progression was:

```
small/basic Lobby seed
        ↓
orientation / classification
        ↓
hypernym + thesaurus network building
        ↓
ר / HypernymStreamComposer
        ↓
complete grammatical propositions
        ↓
candidate abstraction / VGM
```

The rationale was to allow higher-order vocabulary relationships to emerge from a constrained basic vocabulary rather than beginning with a random 1-in-118 sample from a large thesaurus.

### Important qualification

During the original development discussion, the Swadesh list was described as concepts that are universal/cross-linguistically stable and “acquired earliest in childhood.” The **cross-linguistic basic-vocabulary/stability motivation belongs to the Swadesh tradition**, but the stronger developmental claim that the Swadesh list itself is an empirically established list of the earliest-acquired child words should not be attributed to Swadesh without separate evidence. Nelson's first-50-word work provides the direct child-language evidence used alongside it.

Likewise, the project's conclusion that basic-level vocabulary should seed ECHO before abstraction is an engineering hypothesis informed by these sources, not a result established by those sources for artificial systems.

## Why these sources matter to the autonomous-agency record

The small Lobby was not merely an incomplete version of the later large Lobby. It was an experimental starting condition. The research program deliberately juxtaposed:

- child first-word distributions (Nelson),
- vocabulary development through labelling, packaging, and network building (Aitchison),
- a compact cross-linguistic basic-concept inventory (Swadesh), and
- ECHO's own hypernym/thesaurus and ר sentence-composition mechanisms.

Therefore later experiments should distinguish **seed vocabulary**, **network-expanded vocabulary**, and **generated abstractions** rather than treating all Lobby words as if they entered the system at the same developmental stage.
