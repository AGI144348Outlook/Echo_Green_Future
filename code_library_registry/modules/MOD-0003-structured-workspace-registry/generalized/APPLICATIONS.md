# Applications, assumptions and limits

## Applications

- browser or notebook workspaces that organize user-created records before export;
- evidence maps whose relations must reference existing local items;
- small research registries with optional lookup-provider enrichment;
- test fixtures for indexed collections and relationship graphs;
- offline-first drafts that need detached snapshots and atomic JSON replacement;
- prototyping graph-shaped metadata without committing to a database schema.

## Assumptions

- One process owns a workspace instance at a time.
- Provider calls are trusted, bounded and synchronous.
- Payloads, metadata and evidence must be JSON-serializable before saving.
- Collection, item and binding IDs use the documented safe identifier alphabet.
- The filesystem supports same-directory atomic replacement for `os.replace`.

## Limits

This is not a multi-user database, authorization layer, conflict-free replicated data type, transactional graph store or sandbox for untrusted payloads. It has no locking, schema migration, query planner, remote synchronization, cryptographic integrity or crash recovery beyond atomic replacement of one JSON file. In-memory changes made after the last successful save are not durable.

