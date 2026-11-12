-- ECHO-017: persistent, self-directed dictionary-only reinforcement study.
-- Pre-test publication: https://github.com/AGI144348Outlook/Echo_Green_Future/issues/438
-- STRICTLY development branch (lexicon-catalog/echo-card-evidence-dictionary-dev-20261112).
-- This is a Neon-contained algorithmic study engine; it DOES NOT implement an
-- MCP-over-HTTP client. The action names correspond to allowlisted Echo MCP tools.
-- No original WordNet, production warehouse, or existing card/edge is modified.

CREATE SCHEMA IF NOT EXISTS echo_study;

CREATE TABLE IF NOT EXISTS echo_study.configuration (
 config_id integer PRIMARY KEY CHECK (config_id = 1),
 allowed_tools text[] NOT NULL CHECK (
  allowed_tools = ARRAY[
   'dictionary.lexical_path','catalog.card.get',
   'evidence.edge.trace','evidence.edge.propose'
  ]::text[]
 ),
 exploration_factor double precision NOT NULL DEFAULT 0.8
   CHECK (exploration_factor BETWEEN 0 AND 2),
 ema_alpha double precision NOT NULL DEFAULT 0.20
   CHECK (ema_alpha > 0 AND ema_alpha <= 1),
 max_steps_per_round integer NOT NULL DEFAULT 96
   CHECK (max_steps_per_round BETWEEN 1 AND 128),
 active boolean NOT NULL DEFAULT true,
 created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS echo_study.policy_arms (
 action_name text PRIMARY KEY CHECK (action_name IN (
   'dictionary.lexical_path','catalog.card.get',
   'evidence.edge.trace','evidence.edge.propose')),
 attempts bigint NOT NULL DEFAULT 0 CHECK (attempts >= 0),
 total_reward double precision NOT NULL DEFAULT 0,
 ema_reward double precision NOT NULL DEFAULT 0,
 updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS echo_study.progress (
 id integer PRIMARY KEY CHECK(id=1),
 global_step bigint NOT NULL DEFAULT 0,
 pair_cursor bigint NOT NULL DEFAULT 0,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS echo_study.observations (
 action_name text NOT NULL,
 word text NOT NULL,
 first_seen_at timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(action_name, word)
);

CREATE TABLE IF NOT EXISTS echo_study.sessions (
 session_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 started_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 finished_at timestamptz,
 requested_steps integer NOT NULL,
 completed_steps integer NOT NULL DEFAULT 0,
 newly_proposed_edges integer NOT NULL DEFAULT 0,
 refused_candidates integer NOT NULL DEFAULT 0,
 duplicate_candidates integer NOT NULL DEFAULT 0,
 notes text NOT NULL DEFAULT 'source-only intrinsic reinforcement; no verified facts',
 outcome text NOT NULL DEFAULT 'in_progress'
   CHECK(outcome IN ('in_progress','completed','failed','halted'))
);

CREATE TABLE IF NOT EXISTS echo_study.episodes (
 episode_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 session_id bigint NOT NULL REFERENCES echo_study.sessions(session_id),
 global_step bigint NOT NULL UNIQUE,
 action_name text NOT NULL REFERENCES echo_study.policy_arms(action_name),
 source_word text,
 target_word text,
 outcome text NOT NULL,
 reward double precision NOT NULL,
 evidence_edge_id text,
 observations jsonb NOT NULL DEFAULT '{}'::jsonb
   CHECK (jsonb_typeof(observations)='object'),
 recorded_at timestamptz NOT NULL DEFAULT clock_timestamp()
);

-- Keep state shielded from PUBLIC. Application roles get no grants.
REVOKE ALL ON SCHEMA echo_study FROM PUBLIC;
ALTER TABLE echo_study.configuration ENABLE ROW LEVEL SECURITY;
ALTER TABLE echo_study.policy_arms ENABLE ROW LEVEL SECURITY;
ALTER TABLE echo_study.progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE echo_study.observations ENABLE ROW LEVEL SECURITY;
ALTER TABLE echo_study.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE echo_study.episodes ENABLE ROW LEVEL SECURITY;

INSERT INTO echo_study.configuration(config_id, allowed_tools)
 VALUES(1,ARRAY['dictionary.lexical_path','catalog.card.get',
                  'evidence.edge.trace','evidence.edge.propose']::text[])
 ON CONFLICT(config_id) DO NOTHING;
INSERT INTO echo_study.progress(id) VALUES(1) ON CONFLICT DO NOTHING;
INSERT INTO echo_study.policy_arms(action_name)
 VALUES('dictionary.lexical_path'),
       ('catalog.card.get'),
       ('evidence.edge.trace'),
       ('evidence.edge.propose')
 ON CONFLICT DO NOTHING;

CREATE OR REPLACE FUNCTION echo_study.study_round(requested integer DEFAULT 96)
RETURNS jsonb LANGUAGE plpgsql VOLATILE SET search_path=pg_catalog,public,echo_study,card_protocol,evidence_net,echo_dictionary,genesis AS $function$
DECLARE
 cfg echo_study.configuration%ROWTYPE;
 st echo_study.progress%ROWTYPE;
 arm text;
 episode bigint;
 ix integer;
 num_words integer;
 num_pairs integer;
 v_session bigint;
 v_word text;
 v_second text;
 v_left genesis.wordnet_chain%ROWTYPE;
 v_right genesis.wordnet_chain%ROWTYPE;
 v_card_count integer;
 v_edge_count integer;
 v_df integer;
 v_anchor text;
 v_reward double precision;
 v_status text;
 v_edge text;
 v_inserted text;
 v_is_new boolean;
 v_attempts bigint;
 v_ema double precision;
 v_new integer:=0;
 v_refused integer:=0;
 v_dup integer:=0;
 v_read integer:=0;
 v_total bigint;
 v_elapsed double precision;
BEGIN
 -- Only a single study round can mutate the policy at any moment.
 PERFORM pg_advisory_xact_lock(193100017);
 SELECT * INTO cfg FROM echo_study.configuration WHERE config_id=1;
 IF NOT FOUND OR NOT cfg.active THEN
  RETURN jsonb_build_object('status','halted','reason','study not enabled');
 END IF;
 IF requested IS NULL OR requested < 1 OR requested > cfg.max_steps_per_round THEN
  RAISE EXCEPTION 'Study request outside allowed 1..% steps',cfg.max_steps_per_round;
 END IF;
 SELECT * INTO st FROM echo_study.progress WHERE id=1 FOR UPDATE;
 SELECT count(*) INTO num_words FROM echo_dictionary.wordnet_context;
 SELECT count(*) INTO num_pairs
 FROM echo_dictionary.wordnet_context a
 JOIN echo_dictionary.wordnet_context b ON a.word < b.word;
 IF num_words < 2 OR num_pairs < 1 THEN
  RAISE EXCEPTION 'Need at least two admitted, existing dictionary words';
 END IF;
 INSERT INTO echo_study.sessions(requested_steps) VALUES(requested)
 RETURNING session_id INTO v_session;

 FOR ix IN 1..requested LOOP
  SELECT COALESCE(sum(attempts),0) INTO v_total
  FROM echo_study.policy_arms
  WHERE action_name=ANY(cfg.allowed_tools);
  -- A-101-inspired UCB1: choose unexplored arms first, then mean reward plus
  -- exploration bonus. Tie-break by name for deterministic replay.
  SELECT a.action_name INTO arm
  FROM echo_study.policy_arms a
  WHERE a.action_name=ANY(cfg.allowed_tools)
  ORDER BY
    CASE WHEN a.attempts=0 THEN 1000000.0
         ELSE (a.total_reward/a.attempts::double precision) +
           cfg.exploration_factor *
             sqrt(2.0*ln(greatest(1.0,v_total::double precision)+1.0)/
                  a.attempts::double precision)
    END DESC,
    a.action_name ASC
  LIMIT 1;

  SELECT word INTO v_word FROM echo_dictionary.wordnet_context
  ORDER BY word OFFSET ((st.global_step % num_words)::integer) LIMIT 1;
  v_second:=NULL;
  v_anchor:=NULL;
  v_edge:=NULL;
  v_reward:=0.0;
  v_status:='no_new_evidence';

  IF arm='dictionary.lexical_path' THEN
    SELECT * INTO v_left FROM genesis.wordnet_chain WHERE word=v_word;
    IF FOUND AND v_left.synset IS NOT NULL AND
       coalesce(array_length(v_left.chain,1),0)>0 THEN
      INSERT INTO echo_study.observations(action_name,word)
      VALUES(arm,v_word) ON CONFLICT DO NOTHING
      RETURNING true INTO v_is_new;
      IF coalesce(v_is_new,false) THEN v_reward:=0.22;v_status:='first_sourced_dictionary_study';
      ELSE v_reward:=0;v_status:='revisited_dictionary_study';END IF;
    ELSE v_reward:=-0.25;v_status:='missing_source';v_refused:=v_refused+1;END IF;
  ELSIF arm='catalog.card.get' THEN
    SELECT count(*) INTO v_card_count
    FROM card_protocol.card_revisions c
    WHERE c.card_id='lex:'||v_word AND c.revision=1
      AND c.provenance->>'source_table'='genesis.wordnet_chain';
    IF v_card_count=1 THEN
      INSERT INTO echo_study.observations(action_name,word)
      VALUES(arm,v_word) ON CONFLICT DO NOTHING
      RETURNING true INTO v_is_new;
      IF coalesce(v_is_new,false) THEN v_reward:=0.24;v_status:='first_pinned_card_study';
      ELSE v_reward:=0;v_status:='revisited_pinned_card';END IF;
    ELSE v_reward:=-0.35;v_status:='missing_pinned_card';v_refused:=v_refused+1;END IF;
  ELSIF arm='evidence.edge.trace' THEN
    SELECT count(*) INTO v_edge_count
    FROM evidence_net.edges e
    WHERE e.supporting_card_id='lex:'||v_word
      AND e.supporting_card_revision=1
      AND e.source_ref='genesis.wordnet_chain:'||v_word
      AND e.relation_domain='lexical'
      AND e.evidence_state='proposed';
    SELECT * INTO v_left FROM genesis.wordnet_chain WHERE word=v_word;
    IF v_edge_count=coalesce(array_length(v_left.chain,1),0) AND v_edge_count>0 THEN
      INSERT INTO echo_study.observations(action_name,word)
      VALUES(arm,v_word) ON CONFLICT DO NOTHING RETURNING true INTO v_is_new;
      IF coalesce(v_is_new,false) THEN v_reward:=0.28;v_status:='first_source_linked_trace';
      ELSE v_reward:=0;v_status:='revisited_source_trace';END IF;
    ELSE v_reward:=-0.35;v_status:='incomplete_source_trace';v_refused:=v_refused+1;END IF;
  ELSIF arm='evidence.edge.propose' THEN
    -- Pair selection is entirely corpus-driven: no question-by-question
    -- human prompt, no network search, and no use of an external model.
    SELECT a.word,b.word INTO v_word,v_second
    FROM echo_dictionary.wordnet_context a
    JOIN echo_dictionary.wordnet_context b ON a.word<b.word
    ORDER BY a.word,b.word
    OFFSET ((st.pair_cursor%num_pairs)::integer) LIMIT 1;
    st.pair_cursor:=st.pair_cursor+1;
    SELECT * INTO v_left FROM genesis.wordnet_chain WHERE word=v_word;
    SELECT * INTO v_right FROM genesis.wordnet_chain WHERE word=v_second;
    v_edge:='echo017:wordpair:'||v_word||':'||v_second;

    -- Require both exact pinned card revisions and complete source chains.
    SELECT count(*) INTO v_card_count FROM card_protocol.card_revisions
    WHERE card_id IN ('lex:'||v_word,'lex:'||v_second) AND revision=1
      AND provenance->>'source_table'='genesis.wordnet_chain';
    SELECT count(*) INTO v_edge_count FROM evidence_net.edges
    WHERE relation_type='lexical_path'
      AND evidence_state='proposed'
      AND ((supporting_card_id='lex:'||v_word AND supporting_card_revision=1 AND source_ref='genesis.wordnet_chain:'||v_word)
        OR (supporting_card_id='lex:'||v_second AND supporting_card_revision=1 AND source_ref='genesis.wordnet_chain:'||v_second));
    IF v_card_count<>2 OR v_edge_count<>coalesce(array_length(v_left.chain,1),0)+coalesce(array_length(v_right.chain,1),0) THEN
      v_status:='missing_card_or_source_path';v_reward:=-0.3;v_refused:=v_refused+1;
    ELSE
      -- A lexical ancestor is a *candidate source relationship*, NOT a fact.
      -- Reject universal ancestors and high-frequency non-discriminating nodes.
      SELECT x.term,count_check.df INTO v_anchor,v_df
      FROM unnest(v_left.chain) AS x(term)
      CROSS JOIN LATERAL (
        SELECT count(*)::integer AS df FROM genesis.wordnet_chain t
        WHERE x.term=ANY(t.chain)
      ) AS count_check
      WHERE x.term=ANY(v_right.chain)
        AND x.term<>'entity'
        AND (v_left.synset=v_right.synset OR count_check.df <= greatest(2,ceil(num_words*0.25)::integer))
        AND (v_left.synset=v_right.synset OR x.term<>ALL(ARRAY[v_word,v_second]))
      ORDER BY count_check.df, length(x.term) DESC,x.term LIMIT 1;
      IF v_anchor IS NULL THEN
        v_status:='generic_or_unrelated_abstention';v_reward:=0.06;v_refused:=v_refused+1;
      ELSE
        -- Study-created cards are explicitly provisional and pin both source
        -- cards to revision 1. Never rewrite or promote original source cards.
        INSERT INTO card_protocol.card_revisions
         (card_id,revision,card_kind,title,body,provenance,review_state)
        VALUES ('echo017:card:'||v_word||':'||v_second,1,'evidence',
          'Provisional lexical relationship '||v_word||' / '||v_second,
          jsonb_build_object(
            'source_word',v_word,'target_word',v_second,
            'shared_ancestor',v_anchor,'ancestor_frequency',v_df,
            'source_cards',jsonb_build_array(
              jsonb_build_object('id','lex:'||v_word,'revision',1),
              jsonb_build_object('id','lex:'||v_second,'revision',1)),
            'source_synsets',jsonb_build_array(v_left.synset,v_right.synset),
            'admission','none','epistemic_state','provisional'),
          jsonb_build_object('source','genesis.wordnet_chain',
            'engine','ECHO-017-UCB1','method','provisional lexical-ancestor intersection'),
          'proposed') ON CONFLICT DO NOTHING;
        INSERT INTO evidence_net.edges(edge_id,source_node,target_node,relation_type,
          relation_domain,evidence_state,supporting_card_id,supporting_card_revision,source_ref)
        VALUES (v_edge,'word:'||v_word,'word:'||v_second,'shared_lexical_ancestor',
          'lexical','proposed','echo017:card:'||v_word||':'||v_second,1,
          'genesis.wordnet_chain:'||v_word||'|'||v_second)
        ON CONFLICT DO NOTHING RETURNING edge_id INTO v_inserted;
        IF v_inserted IS NOT NULL THEN
          INSERT INTO evidence_net.edge_sources(edge_id,source_node,support_kind)
          VALUES (v_edge,'word:'||v_word,'derived_from'),(v_edge,'word:'||v_second,'derived_from')
          ON CONFLICT DO NOTHING;
          v_status:='new_provisional_relation';
          v_reward:=0.5+0.4*(1.0-v_df::double precision/num_words::double precision);
          v_new:=v_new+1;
        ELSE
          v_status:='existing_relation_no_novelty';v_reward:=-0.08;v_dup:=v_dup+1;
        END IF;
      END IF;
    END IF;
  ELSE
    RAISE EXCEPTION 'Tool outside the four allowed dictionary/card/evidence capabilities';
  END IF;

  INSERT INTO echo_study.episodes(session_id,global_step,action_name,source_word,
    target_word,outcome,reward,evidence_edge_id,observations)
  VALUES(v_session,st.global_step,arm,v_word,v_second,v_status,v_reward,
      CASE WHEN v_status='new_provisional_relation' THEN v_edge ELSE NULL END,
      jsonb_build_object('ancestor',v_anchor,'source','genesis.wordnet_chain',
        'epistemic_state','provisional','authority_granted',false,'admitted_words',0));

  UPDATE echo_study.policy_arms
    SET ema_reward=CASE WHEN attempts=0 THEN v_reward
      ELSE cfg.ema_alpha*v_reward+(1-cfg.ema_alpha)*ema_reward END,
        attempts=attempts+1,total_reward=total_reward+v_reward,
        updated_at=clock_timestamp()
  WHERE action_name=arm;
  st.global_step:=st.global_step+1;
 END LOOP;

 UPDATE echo_study.progress
 SET global_step=st.global_step,pair_cursor=st.pair_cursor,
     updated_at=clock_timestamp() WHERE id=1;
 UPDATE echo_study.sessions SET
 completed_steps=requested, newly_proposed_edges=v_new,
 refused_candidates=v_refused, duplicate_candidates=v_dup,
 finished_at=clock_timestamp(), outcome='completed'
 WHERE session_id=v_session;
 SELECT extract(epoch FROM finished_at-started_at)
 INTO v_elapsed FROM echo_study.sessions WHERE session_id=v_session;
 RETURN jsonb_build_object(
  'session_id',v_session,'status','completed','requested_steps',requested,
  'completed_steps',requested,'total_steps',st.global_step,
  'pair_attempts',st.pair_cursor,'new_provisional_relations',v_new,
  'refused_candidates',v_refused,'duplicates',v_dup,
  'elapsed_wall_seconds',v_elapsed,
  'tool_allowlist',cfg.allowed_tools,
  'intrinsic_reward_is_proxy_not_truth',true,
  'scope','isolated Neon child branch; no live MCP HTTP'
 );
END;
$function$;

-- Database owners execute directly for experiments. No EXECUTE privilege for
-- anonymous or general-purpose accounts; this is not an exposed MCP tool.
REVOKE ALL ON FUNCTION echo_study.study_round(integer) FROM PUBLIC;
