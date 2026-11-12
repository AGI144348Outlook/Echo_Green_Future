-- Additive versioned index-card catalog and evidence network, development-branch only.
-- Existing nb.*, public.card, genesis.*, and core_lexicon.* are untouched.
-- Cards are inert: neither state nor stamp metadata grants operational authority.
CREATE SCHEMA IF NOT EXISTS card_protocol;
CREATE SCHEMA IF NOT EXISTS evidence_net;

CREATE TABLE IF NOT EXISTS card_protocol.card_revisions (
 card_id text NOT NULL CHECK (length(card_id) BETWEEN 1 AND 128),
 revision integer NOT NULL CHECK (revision > 0),
 card_kind text NOT NULL CHECK (card_kind IN ('evidence','seat_charter','tool','route_ticket','communication','action','approval_reference','authority_stamp','detour','lexical_context')),
 title text NOT NULL CHECK (length(trim(title)) > 0),
 body jsonb NOT NULL CHECK (jsonb_typeof(body) = 'object'),
 provenance jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(provenance)='object'),
 review_state text NOT NULL DEFAULT 'proposed' CHECK (review_state IN ('proposed','reviewed','contested','rejected')),
 created_at timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(card_id, revision)
);
CREATE TABLE IF NOT EXISTS card_protocol.configuration_revisions (
 config_id text NOT NULL,
 revision integer NOT NULL CHECK (revision > 0),
 title text NOT NULL,
 mission_ref text,
 config_data jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(config_data)='object'),
 created_at timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(config_id,revision)
);
CREATE TABLE IF NOT EXISTS card_protocol.configuration_members (
 config_id text NOT NULL,
 config_revision integer NOT NULL,
 card_id text NOT NULL,
 card_revision integer NOT NULL,
 ordinal integer NOT NULL CHECK (ordinal >= 0),
 PRIMARY KEY(config_id, config_revision, card_id, card_revision),
 UNIQUE(config_id,config_revision,ordinal),
 FOREIGN KEY(config_id,config_revision) REFERENCES card_protocol.configuration_revisions(config_id,revision),
 FOREIGN KEY(card_id,card_revision) REFERENCES card_protocol.card_revisions(card_id,revision)
);
CREATE TABLE IF NOT EXISTS card_protocol.evaluation_receipts (
 receipt_id text PRIMARY KEY,
 config_id text,
 config_revision integer,
 mission_ref text NOT NULL,
 actor_ref text NOT NULL,
 requested_action text NOT NULL,
 decision text NOT NULL CHECK (decision IN ('denied','eligible_nonexecuting','eligible_pending_external_authorization')),
 reason text NOT NULL,
 result jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(result)='object'),
 recorded_at timestamptz NOT NULL DEFAULT now(),
 FOREIGN KEY(config_id,config_revision) REFERENCES card_protocol.configuration_revisions(config_id,revision),
 CHECK ((config_id IS NULL AND config_revision IS NULL) OR (config_id IS NOT NULL AND config_revision IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS evidence_net.nodes (
 node_id text PRIMARY KEY,
 node_kind text NOT NULL CHECK (node_kind IN ('source','claim','concept','observation','lexical_sense','experiment')),
 label text NOT NULL,
 details jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(details)='object'),
 attribution_ref text,
 evidence_state text NOT NULL DEFAULT 'provisional' CHECK(evidence_state IN ('provisional','contested','reviewed','rejected')),
 recorded_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS evidence_net.edges (
 edge_id text PRIMARY KEY,
 source_node text NOT NULL REFERENCES evidence_net.nodes(node_id),
 target_node text NOT NULL REFERENCES evidence_net.nodes(node_id),
 relation_type text NOT NULL CHECK(length(trim(relation_type)) > 0),
 relation_domain text NOT NULL CHECK(relation_domain IN ('lexical','empirical','operational')),
 evidence_state text NOT NULL DEFAULT 'proposed' CHECK(evidence_state IN ('proposed','contested','reviewed','rejected')),
 supporting_card_id text,
 supporting_card_revision integer,
 source_ref text,
 recorded_at timestamptz NOT NULL DEFAULT now(),
 FOREIGN KEY(supporting_card_id,supporting_card_revision) REFERENCES card_protocol.card_revisions(card_id,revision),
 CHECK ((supporting_card_id IS NULL AND supporting_card_revision IS NULL) OR (supporting_card_id IS NOT NULL AND supporting_card_revision IS NOT NULL))
);
CREATE TABLE IF NOT EXISTS evidence_net.edge_sources (
 edge_id text NOT NULL REFERENCES evidence_net.edges(edge_id),
 source_node text NOT NULL REFERENCES evidence_net.nodes(node_id),
 support_kind text NOT NULL CHECK(support_kind IN ('supports','contradicts','contextualizes','derived_from')),
 PRIMARY KEY(edge_id,source_node,support_kind)
);
CREATE TABLE IF NOT EXISTS evidence_net.edge_assessments (
 assessment_id text PRIMARY KEY,
 edge_id text NOT NULL REFERENCES evidence_net.edges(edge_id),
 reviewer_ref text NOT NULL,
 decision text NOT NULL CHECK(decision IN ('accept_for_review','reject','dispute','request_evidence')),
 rationale text NOT NULL,
 source_ref text,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS evidence_net_edges_source_idx ON evidence_net.edges(source_node, relation_type, relation_domain);
CREATE INDEX IF NOT EXISTS evidence_net_edges_target_idx ON evidence_net.edges(target_node, relation_type, relation_domain);
CREATE INDEX IF NOT EXISTS card_protocol_cards_kind_idx ON card_protocol.card_revisions(card_kind,card_id,revision);

-- Guard the added schemas against public SQL access; actual service credentials
-- and per-seat RLS policies require a separate approved enforcement design.
REVOKE ALL ON SCHEMA card_protocol FROM PUBLIC;
REVOKE ALL ON SCHEMA evidence_net FROM PUBLIC;
ALTER TABLE card_protocol.card_revisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE card_protocol.configuration_revisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE card_protocol.configuration_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE card_protocol.evaluation_receipts ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence_net.nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence_net.edges ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence_net.edge_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence_net.edge_assessments ENABLE ROW LEVEL SECURITY;
