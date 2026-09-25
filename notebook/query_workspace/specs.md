# Notebook Query Workspace — specs

## Purpose
Echo's notebook is a persistent address-space/workbench, not a duplicate database. It resolves registry handles and may assemble temporary matrices from permanent registries for a current task.

## Query primitive

\`Q(sources, predicate, projection) -> M_Q\`

- **sources**: one or more registries/matrices referenced by notebook handles.
- **predicate**: constraints used to select records.
- **projection**: fields/relations to expose.
- **M_Q**: a temporary matrix instantiated for the query.

## Lifetimes
1. **discard** — transient result ends with the working operation.
2. **retain** — keep the result in the notebook working space.
3. **saved view** — persist the construction rule so it can be reconstructed from current registry state.
4. **submit for validation** — candidate generalization may be evaluated for VGM admission.

Saving is not validation. No temporary matrix or saved view enters the VGM merely because Echo retains it.

## Generalization Registry tool
- Registry: \`registries/generalization_registry.json\`
- Index: \`indices/generalization_registry_index.json\`
- Cardinality: 22 glyphs × 4 grammatical roles = 88 unique handles.
- Roles: noun, verb, adjective, adverb.
- Lookup paths: glyph → handles; word → glyph/role/operator; role → 22 words.
- Separation: this registry does not define glyph semantics and does not modify the VGM.

### Example
\`through\` resolves through the word index to glyph \`ג\`, role \`adverb\`, operator label \`TRAVERSE\`. A notebook query may combine that result with other registry records to construct a temporary matrix without copying the source registries.

## Governance
Resolution is not authorization. Existing notebook rule \`OPEN(handle)\` remains separately governed by ר.
