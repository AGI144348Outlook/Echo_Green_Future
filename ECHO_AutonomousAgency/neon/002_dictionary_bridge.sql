-- Echo ONLY: expose the existing dictionary as a read-only lexical context.
-- WordNet table remains canonical; no copy is made by this view.
CREATE SCHEMA IF NOT EXISTS echo_dictionary;
CREATE OR REPLACE VIEW echo_dictionary.wordnet_context AS
SELECT word, synset, definition, chain, depth
FROM genesis.wordnet_chain;
REVOKE ALL ON SCHEMA echo_dictionary FROM PUBLIC;
