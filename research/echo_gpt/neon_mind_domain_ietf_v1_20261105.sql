-- Additive Mind Domain / IETF organizational model. Does not modify entropy policy.
CREATE TABLE IF NOT EXISTS echo_warehouse.mind_domains (
 domain_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 parent_domain_id bigint REFERENCES echo_warehouse.mind_domains(domain_id),
 domain_key text NOT NULL UNIQUE,
 domain_kind text NOT NULL CHECK(domain_kind IN ('mind','knowledge','memory','thinking','imagination','introspection','contemplation','temporary','meta')),
 label text NOT NULL,
 is_experimental boolean NOT NULL DEFAULT false,
 created_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO echo_warehouse.mind_domains(domain_key,domain_kind,label) VALUES
 ('echo.mind','mind','Echo Mind Domain'),
 ('echo.knowledge','knowledge','Knowledge'),
 ('echo.memory','memory','Memory'),
 ('echo.thinking','thinking','Thinking'),
 ('echo.imagination','imagination','Imagination'),
 ('echo.introspection','introspection','Introspection'),
 ('echo.contemplation','contemplation','Contemplation')
ON CONFLICT(domain_key) DO NOTHING;
UPDATE echo_warehouse.mind_domains SET parent_domain_id=(SELECT domain_id FROM echo_warehouse.mind_domains WHERE domain_key='echo.mind') WHERE domain_key IN ('echo.knowledge','echo.memory','echo.thinking','echo.imagination','echo.introspection','echo.contemplation') AND parent_domain_id IS NULL;
CREATE TABLE IF NOT EXISTS echo_warehouse.box_domain_membership (
 box_id bigint NOT NULL REFERENCES echo_warehouse.boxes(box_id) ON DELETE CASCADE,
 domain_id bigint NOT NULL REFERENCES echo_warehouse.mind_domains(domain_id),
 assigned_at timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(box_id,domain_id)
);
CREATE TABLE IF NOT EXISTS echo_warehouse.ietf_templates (
 template_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 domain_id bigint NOT NULL REFERENCES echo_warehouse.mind_domains(domain_id),
 template_key text NOT NULL UNIQUE,
 rules jsonb NOT NULL DEFAULT '{}'::jsonb,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS echo_warehouse.ietf_nodes (
 node_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 domain_id bigint NOT NULL REFERENCES echo_warehouse.mind_domains(domain_id),
 template_id bigint REFERENCES echo_warehouse.ietf_templates(template_id),
 parent_node_id bigint REFERENCES echo_warehouse.ietf_nodes(node_id),
 configuration jsonb NOT NULL DEFAULT '{}'::jsonb,
 local_time numeric NOT NULL DEFAULT 0,
 time_mode text NOT NULL DEFAULT 'frozen' CHECK(time_mode IN ('frozen','forward','accelerated','decelerated','reversible')),
 status text NOT NULL DEFAULT 'proposed' CHECK(status IN ('proposed','running','completed','aborted')),
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS echo_warehouse.ietf_snapshots (
 snapshot_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 node_id bigint NOT NULL REFERENCES echo_warehouse.ietf_nodes(node_id),
 local_time numeric NOT NULL,
 state jsonb NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS echo_warehouse.ietf_results (
 result_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 node_id bigint NOT NULL REFERENCES echo_warehouse.ietf_nodes(node_id),
 snapshot_id bigint REFERENCES echo_warehouse.ietf_snapshots(snapshot_id),
 observation jsonb NOT NULL,
 interpretation jsonb NOT NULL DEFAULT '{}'::jsonb,
 evidence_uri text,
 verification_status text NOT NULL DEFAULT 'unverified' CHECK(verification_status IN ('unverified','rejected','verified')),
 created_at timestamptz NOT NULL DEFAULT now()
);
REVOKE ALL ON echo_warehouse.mind_domains,echo_warehouse.box_domain_membership,echo_warehouse.ietf_templates,echo_warehouse.ietf_nodes,echo_warehouse.ietf_snapshots,echo_warehouse.ietf_results FROM PUBLIC;
GRANT SELECT ON echo_warehouse.mind_domains TO echo_agent_api;
