-- Echo-GPT Neon warehouse v1. Non-destructive; canonical entropy is externally governed.
CREATE SCHEMA IF NOT EXISTS echo_warehouse;
CREATE TABLE IF NOT EXISTS echo_warehouse.policy (
 id smallint PRIMARY KEY DEFAULT 1 CHECK (id=1),
 entropy_amplitude numeric(8,6) NOT NULL DEFAULT 0.034 CHECK(entropy_amplitude BETWEEN 0.032 AND 0.036),
 wave_factor numeric(8,6) NOT NULL DEFAULT 0.25 CHECK(wave_factor BETWEEN 0 AND 1),
 tick_period text NOT NULL DEFAULT 'externally triggered',
 revision bigint NOT NULL DEFAULT 1,
 updated_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO echo_warehouse.policy(id) VALUES (1) ON CONFLICT (id) DO NOTHING;
CREATE TABLE IF NOT EXISTS echo_warehouse.boxes (
 box_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 generation integer NOT NULL DEFAULT 0,
 payload jsonb NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(),
 created_tick bigint NOT NULL DEFAULT 0,
 last_maintained_tick bigint NOT NULL DEFAULT 0,
 accessibility double precision NOT NULL DEFAULT 1 CHECK(accessibility BETWEEN 0 AND 1),
 status text NOT NULL DEFAULT 'active' CHECK(status IN ('active','inaccessible')),
 provenance text
);
CREATE TABLE IF NOT EXISTS echo_warehouse.ties (
 tie_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 from_box bigint NOT NULL REFERENCES echo_warehouse.boxes(box_id),
 to_box bigint NOT NULL REFERENCES echo_warehouse.boxes(box_id),
 relation jsonb NOT NULL DEFAULT '{}'::jsonb,
 strength double precision NOT NULL DEFAULT 1 CHECK(strength BETWEEN 0 AND 1),
 phase double precision NOT NULL DEFAULT 0,
 created_tick bigint NOT NULL DEFAULT 0,
 last_maintained_tick bigint NOT NULL DEFAULT 0,
 UNIQUE(from_box,to_box), CHECK(from_box<>to_box)
);
CREATE TABLE IF NOT EXISTS echo_warehouse.clock (
 id smallint PRIMARY KEY DEFAULT 1 CHECK(id=1),
 tick bigint NOT NULL DEFAULT 0 CHECK(tick>=0),
 updated_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO echo_warehouse.clock(id) VALUES(1) ON CONFLICT(id) DO NOTHING;
CREATE TABLE IF NOT EXISTS echo_warehouse.events (
 event_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 recorded_at timestamptz NOT NULL DEFAULT now(),
 tick bigint NOT NULL,
 kind text NOT NULL,
 box_id bigint,
 tie_id bigint,
 details jsonb NOT NULL DEFAULT '{}'::jsonb
);
CREATE TABLE IF NOT EXISTS echo_warehouse.scoring_ledger (
 score_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 created_at timestamptz NOT NULL DEFAULT now(),
 tick bigint NOT NULL,
 evaluation_kind text NOT NULL,
 result jsonb NOT NULL
);
CREATE INDEX IF NOT EXISTS warehouse_boxes_generation ON echo_warehouse.boxes(generation);
CREATE INDEX IF NOT EXISTS warehouse_ties_from ON echo_warehouse.ties(from_box);
CREATE INDEX IF NOT EXISTS warehouse_ties_to ON echo_warehouse.ties(to_box);
CREATE OR REPLACE VIEW echo_warehouse.accessible_boxes AS
 SELECT box_id,generation,payload,accessibility,created_tick FROM echo_warehouse.boxes
 WHERE status='active' AND accessibility>=0.38;
CREATE OR REPLACE VIEW echo_warehouse.accessible_ties AS
 SELECT t.tie_id,t.from_box,t.to_box,t.relation,t.strength,t.phase
 FROM echo_warehouse.ties t JOIN echo_warehouse.boxes a ON a.box_id=t.from_box
 JOIN echo_warehouse.boxes b ON b.box_id=t.to_box
 WHERE t.strength>=0.38 AND a.accessibility>=0.38 AND b.accessibility>=0.38
 AND a.status='active' AND b.status='active';
-- A dedicated no-login role is the least-privilege access surface for an agent session.
DO $$ BEGIN IF NOT EXISTS(SELECT 1 FROM pg_roles WHERE rolname='echo_warehouse_agent') THEN
 CREATE ROLE echo_warehouse_agent NOLOGIN;
 END IF; END $$;
REVOKE ALL ON SCHEMA echo_warehouse FROM PUBLIC;
GRANT USAGE ON SCHEMA echo_warehouse TO echo_warehouse_agent;
GRANT SELECT ON echo_warehouse.accessible_boxes,echo_warehouse.accessible_ties TO echo_warehouse_agent;
-- Views are owned by the deploying administrator. No table access or entropy-setting grants to agent.
CREATE OR REPLACE FUNCTION echo_warehouse.apply_entropy_tick()
RETURNS bigint LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,echo_warehouse AS $$
DECLARE t bigint; amp double precision; wf double precision; field double precision;
BEGIN
 SELECT tick+1 INTO t FROM echo_warehouse.clock WHERE id=1 FOR UPDATE;
 SELECT entropy_amplitude::double precision,wave_factor::double precision INTO amp,wf FROM echo_warehouse.policy WHERE id=1;
 field:=amp*(1+wf*sin(t*0.63));
 UPDATE echo_warehouse.boxes SET accessibility=greatest(0,accessibility-field),
 status=CASE WHEN greatest(0,accessibility-field)<0.38 THEN 'inaccessible' ELSE 'active' END;
 UPDATE echo_warehouse.ties SET strength=greatest(0,strength-field*0.8);
 UPDATE echo_warehouse.clock SET tick=t,updated_at=now() WHERE id=1;
 INSERT INTO echo_warehouse.events(tick,kind,details) VALUES(t,'entropy_tick',jsonb_build_object('field',field,'amplitude',amp,'affected_boxes',(SELECT count(*) FROM echo_warehouse.boxes),'affected_ties',(SELECT count(*) FROM echo_warehouse.ties)));
 RETURN t;
END $$;
REVOKE ALL ON FUNCTION echo_warehouse.apply_entropy_tick() FROM PUBLIC;
-- Only the trusted administrator / external scheduler may execute the entropy tick.
