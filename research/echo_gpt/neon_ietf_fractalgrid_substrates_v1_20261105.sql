-- FractalGrid IETF v1. One independent substrate per cognitive subdomain.
CREATE TABLE IF NOT EXISTS echo_warehouse.ietf_substrates (
 substrate_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 domain_id bigint NOT NULL UNIQUE REFERENCES echo_warehouse.mind_domains(domain_id),
 substrate_kind text NOT NULL DEFAULT 'fractalgrid-ietf-v1',
 canonical_frame jsonb NOT NULL DEFAULT '{"origin":[0,0,0],"axes":["x","y","z"]}'::jsonb,
 grid_dimensions integer[] NOT NULL DEFAULT ARRAY[3,3,3],
 configuration jsonb NOT NULL DEFAULT '{}'::jsonb,
 created_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(substrate_id,domain_id),
 CHECK(array_length(grid_dimensions,1)=3 AND grid_dimensions[1]>0 AND grid_dimensions[2]>0 AND grid_dimensions[3]>0)
);
INSERT INTO echo_warehouse.ietf_substrates(domain_id,configuration)
SELECT domain_id,jsonb_build_object('source','CLR-0009,CLR-0011,CLR-0012,CLR-0039,CLR-0024,CLR-0038','canonical_entropy_independent',true)
FROM echo_warehouse.mind_domains WHERE domain_kind IN ('knowledge','memory','thinking','imagination','introspection','contemplation')
ON CONFLICT(domain_id) DO NOTHING;
CREATE TABLE IF NOT EXISTS echo_warehouse.fractal_cells (
 cell_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 substrate_id bigint NOT NULL REFERENCES echo_warehouse.ietf_substrates(substrate_id),
 parent_cell_id bigint,
 depth integer NOT NULL DEFAULT 0 CHECK(depth>=0 AND depth<=64),
 coordinate integer[] NOT NULL CHECK(array_length(coordinate,1)=3),
 local_frame jsonb NOT NULL DEFAULT '{}'::jsonb,
 state jsonb NOT NULL DEFAULT '{}'::jsonb,
 UNIQUE(cell_id,substrate_id),
 UNIQUE(substrate_id,parent_cell_id,coordinate),
 FOREIGN KEY(parent_cell_id,substrate_id) REFERENCES echo_warehouse.fractal_cells(cell_id,substrate_id)
);
CREATE TABLE IF NOT EXISTS echo_warehouse.fractal_scale_specs (
 scale_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 substrate_id bigint NOT NULL REFERENCES echo_warehouse.ietf_substrates(substrate_id),
 scale_key text NOT NULL,
 representation jsonb NOT NULL DEFAULT '{}'::jsonb,
 resolution numeric NOT NULL CHECK(resolution>0),
 cost_model jsonb NOT NULL DEFAULT '{}'::jsonb,
 UNIQUE(scale_id,substrate_id),
 UNIQUE(substrate_id,scale_key)
);
CREATE TABLE IF NOT EXISTS echo_warehouse.fractal_transitions (
 transition_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 substrate_id bigint NOT NULL REFERENCES echo_warehouse.ietf_substrates(substrate_id),
 source_scale_id bigint NOT NULL,
 target_scale_id bigint NOT NULL,
 transform_spec jsonb NOT NULL,
 information_loss jsonb NOT NULL DEFAULT '{}'::jsonb,
 reversibility text NOT NULL DEFAULT 'unknown' CHECK(reversibility IN ('unknown','reversible','lossy')),
 FOREIGN KEY(source_scale_id,substrate_id) REFERENCES echo_warehouse.fractal_scale_specs(scale_id,substrate_id),
 FOREIGN KEY(target_scale_id,substrate_id) REFERENCES echo_warehouse.fractal_scale_specs(scale_id,substrate_id),
 UNIQUE(substrate_id,source_scale_id,target_scale_id)
);
CREATE TABLE IF NOT EXISTS echo_warehouse.fractal_templates (
 fractal_template_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 substrate_id bigint NOT NULL REFERENCES echo_warehouse.ietf_substrates(substrate_id),
 template_key text NOT NULL,
 definition jsonb NOT NULL,
 provenance text NOT NULL DEFAULT 'proposed',
 UNIQUE(fractal_template_id,substrate_id),
 UNIQUE(substrate_id,template_key)
);
CREATE TABLE IF NOT EXISTS echo_warehouse.fractal_instances (
 instance_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 substrate_id bigint NOT NULL REFERENCES echo_warehouse.ietf_substrates(substrate_id),
 fractal_template_id bigint NOT NULL,
 cell_id bigint,
 parent_instance_id bigint,
 transform jsonb NOT NULL DEFAULT '{}'::jsonb,
 local_state jsonb NOT NULL DEFAULT '{}'::jsonb,
 FOREIGN KEY(fractal_template_id,substrate_id) REFERENCES echo_warehouse.fractal_templates(fractal_template_id,substrate_id),
 FOREIGN KEY(cell_id,substrate_id) REFERENCES echo_warehouse.fractal_cells(cell_id,substrate_id),
 FOREIGN KEY(parent_instance_id,substrate_id) REFERENCES echo_warehouse.fractal_instances(instance_id,substrate_id),
 UNIQUE(instance_id,substrate_id)
);
CREATE TABLE IF NOT EXISTS echo_warehouse.fractal_placements (
 placement_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 substrate_id bigint NOT NULL REFERENCES echo_warehouse.ietf_substrates(substrate_id),
 cell_id bigint NOT NULL,
 box_id bigint REFERENCES echo_warehouse.boxes(box_id),
 instance_id bigint,
 canonical_position numeric[] NOT NULL CHECK(array_length(canonical_position,1)=3),
 frame_transform jsonb NOT NULL DEFAULT '{}'::jsonb,
 viewport_state jsonb NOT NULL DEFAULT '{}'::jsonb,
 FOREIGN KEY(cell_id,substrate_id) REFERENCES echo_warehouse.fractal_cells(cell_id,substrate_id),
 FOREIGN KEY(instance_id,substrate_id) REFERENCES echo_warehouse.fractal_instances(instance_id,substrate_id),
 CHECK(box_id IS NOT NULL OR instance_id IS NOT NULL)
);
CREATE TABLE IF NOT EXISTS echo_warehouse.fractal_node_bindings (
 node_id bigint PRIMARY KEY REFERENCES echo_warehouse.ietf_nodes(node_id),
 substrate_id bigint NOT NULL REFERENCES echo_warehouse.ietf_substrates(substrate_id),
 cell_id bigint,
 FOREIGN KEY(cell_id,substrate_id) REFERENCES echo_warehouse.fractal_cells(cell_id,substrate_id)
);
CREATE TABLE IF NOT EXISTS echo_warehouse.fractal_operations (
 operation_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 substrate_id bigint NOT NULL REFERENCES echo_warehouse.ietf_substrates(substrate_id),
 node_id bigint REFERENCES echo_warehouse.ietf_nodes(node_id),
 operation_kind text NOT NULL CHECK(operation_kind IN ('recenter','contract','scale_transition','instantiate','place','other')),
 parameters jsonb NOT NULL DEFAULT '{}'::jsonb,
 observation jsonb NOT NULL DEFAULT '{}'::jsonb,
 verification_status text NOT NULL DEFAULT 'unverified' CHECK(verification_status IN ('unverified','rejected','verified')),
 created_at timestamptz NOT NULL DEFAULT now()
);
REVOKE ALL ON echo_warehouse.ietf_substrates,echo_warehouse.fractal_cells,echo_warehouse.fractal_scale_specs,echo_warehouse.fractal_transitions,echo_warehouse.fractal_templates,echo_warehouse.fractal_instances,echo_warehouse.fractal_placements,echo_warehouse.fractal_node_bindings,echo_warehouse.fractal_operations FROM PUBLIC;
GRANT SELECT ON echo_warehouse.ietf_substrates TO echo_agent_api;
