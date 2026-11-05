-- FractalGrid coordinate hardening; executed against echo_warehouse on 2026-11-05.
-- Prereq: neon_ietf_fractalgrid_substrates_v1_20261105.sql and prior coordinate-tag/avatars additions.
-- The DDL below documents successfully applied changes; it is a reconstruction of commands run through Neon.
CREATE UNIQUE INDEX IF NOT EXISTS fractal_root_per_substrate_uq ON echo_warehouse.fractal_cells (substrate_id) WHERE parent_cell_id IS NULL;
CREATE UNIQUE INDEX IF NOT EXISTS fractal_cell_tag_uq ON echo_warehouse.fractal_cells (coordinate_tag);
ALTER TABLE echo_warehouse.fractal_node_bindings ADD COLUMN IF NOT EXISTS domain_id bigint;
UPDATE echo_warehouse.fractal_node_bindings b SET domain_id = n.domain_id FROM echo_warehouse.ietf_nodes n WHERE n.node_id=b.node_id AND b.domain_id IS NULL;
ALTER TABLE echo_warehouse.fractal_node_bindings ADD CONSTRAINT fractal_binding_node_domain_fk FOREIGN KEY (node_id,domain_id) REFERENCES echo_warehouse.ietf_nodes(node_id,domain_id);
ALTER TABLE echo_warehouse.fractal_node_bindings ADD CONSTRAINT fractal_binding_substrate_domain_fk FOREIGN KEY (substrate_id,domain_id) REFERENCES echo_warehouse.ietf_substrates(substrate_id,domain_id);
ALTER TABLE echo_warehouse.fractal_node_bindings ALTER COLUMN domain_id SET NOT NULL;
ALTER TABLE echo_warehouse.fractal_avatars ADD CONSTRAINT avatar_position_three_axes CHECK (array_length(position,1)=3);
ALTER TABLE echo_warehouse.fractal_avatars ADD CONSTRAINT avatar_mode_enum CHECK (mode IN ('inactive','observing','navigating','paused'));
ALTER TABLE echo_warehouse.fractal_avatars ADD CONSTRAINT avatar_location_pair CHECK ((substrate_id IS NULL AND cell_id IS NULL) OR (substrate_id IS NOT NULL AND cell_id IS NOT NULL));
CREATE UNIQUE INDEX IF NOT EXISTS fractal_placements_coordinate_tag_uq ON echo_warehouse.fractal_placements (coordinate_tag);
REVOKE ALL PRIVILEGES ON TABLE echo_warehouse.fractal_avatars FROM PUBLIC;
CREATE OR REPLACE FUNCTION echo_warehouse.fractal_cell_address() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE parent_depth integer;
BEGIN
 IF NEW.parent_cell_id IS NULL THEN
  IF NEW.depth <> 0 THEN RAISE EXCEPTION 'root depth must be zero'; END IF;
  NEW.coordinate_tag := 'FG:'||NEW.substrate_id||':ROOT:('||array_to_string(NEW.coordinate,',')||')';
 ELSE
  SELECT depth INTO parent_depth FROM echo_warehouse.fractal_cells WHERE cell_id=NEW.parent_cell_id AND substrate_id=NEW.substrate_id;
  IF parent_depth IS NULL OR NEW.depth <> parent_depth+1 THEN RAISE EXCEPTION 'invalid cell ancestry'; END IF;
  NEW.coordinate_tag := 'FG:'||NEW.substrate_id||':CELL:'||NEW.parent_cell_id||':('||array_to_string(NEW.coordinate,',')||')';
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER fractal_cell_address_trigger BEFORE INSERT OR UPDATE OF substrate_id,parent_cell_id,coordinate,depth ON echo_warehouse.fractal_cells FOR EACH ROW EXECUTE FUNCTION echo_warehouse.fractal_cell_address();
-- Existing root rows were retagged with UPDATE fractal_cells SET coordinate=coordinate WHERE parent_cell_id IS NULL.
ALTER TABLE echo_warehouse.fractal_cells ALTER COLUMN coordinate_tag SET NOT NULL;
CREATE OR REPLACE FUNCTION echo_warehouse.fractal_placement_address() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 NEW.coordinate_tag := 'FG:'||NEW.substrate_id||':CELL:'||NEW.cell_id||':P:'||NEW.placement_id||':('||array_to_string(NEW.canonical_position,',')||')';
 RETURN NEW;
END $$;
CREATE TRIGGER fractal_placement_address_trigger BEFORE INSERT OR UPDATE OF substrate_id,cell_id,canonical_position ON echo_warehouse.fractal_placements FOR EACH ROW EXECUTE FUNCTION echo_warehouse.fractal_placement_address();
CREATE OR REPLACE FUNCTION echo_warehouse.fractal_avatar_address() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.cell_id IS NULL THEN NEW.coordinate_tag := NULL;
 ELSE NEW.coordinate_tag := 'FG:'||NEW.substrate_id||':CELL:'||NEW.cell_id||':A:'||NEW.avatar_key||':('||array_to_string(NEW.position,',')||')'; END IF;
 NEW.updated_at := now();
 RETURN NEW;
END $$;
CREATE TRIGGER fractal_avatar_address_trigger BEFORE INSERT OR UPDATE OF substrate_id,cell_id,position,orientation,mode ON echo_warehouse.fractal_avatars FOR EACH ROW EXECUTE FUNCTION echo_warehouse.fractal_avatar_address();
CREATE OR REPLACE VIEW echo_warehouse.fractal_topology AS SELECT d.domain_key,s.substrate_id,c.cell_id,c.parent_cell_id,c.depth,c.coordinate,c.coordinate_tag,c.local_frame FROM echo_warehouse.fractal_cells c JOIN echo_warehouse.ietf_substrates s ON s.substrate_id=c.substrate_id JOIN echo_warehouse.mind_domains d ON d.domain_id=s.domain_id;
ALTER TABLE echo_warehouse.fractal_placements ADD CONSTRAINT fractal_placement_position_not_null_tag CHECK (coordinate_tag IS NOT NULL);
ALTER TABLE echo_warehouse.fractal_avatars ADD CONSTRAINT avatar_address_if_placed CHECK ((cell_id IS NULL AND coordinate_tag IS NULL) OR (cell_id IS NOT NULL AND coordinate_tag IS NOT NULL));
REVOKE ALL PRIVILEGES ON TABLE echo_warehouse.fractal_topology FROM PUBLIC;
GRANT SELECT ON echo_warehouse.fractal_topology TO echo_agent_api;
