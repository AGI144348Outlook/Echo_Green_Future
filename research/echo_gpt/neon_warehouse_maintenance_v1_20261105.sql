CREATE OR REPLACE FUNCTION echo_warehouse.reinforce(p_kind text,p_id bigint,p_amount double precision DEFAULT 0.10) RETURNS boolean
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,echo_warehouse AS $$
DECLARE current_tick bigint; used integer; affected integer;
BEGIN
 IF p_kind NOT IN ('box','tie') OR p_amount<=0 OR p_amount>0.10 THEN RAISE EXCEPTION 'invalid maintenance request'; END IF;
 SELECT tick INTO current_tick FROM echo_warehouse.clock WHERE id=1 FOR UPDATE;
 SELECT count(*) INTO used FROM echo_warehouse.events WHERE tick=current_tick AND kind='maintenance';
 IF used>=5 THEN RAISE EXCEPTION 'maintenance budget exhausted at tick %',current_tick; END IF;
 IF p_kind='box' THEN
  UPDATE echo_warehouse.boxes SET accessibility=least(1,accessibility+p_amount),last_maintained_tick=current_tick,status=CASE WHEN least(1,accessibility+p_amount)>=0.38 THEN 'active' ELSE 'inaccessible' END WHERE box_id=p_id;
 ELSE
  UPDATE echo_warehouse.ties SET strength=least(1,strength+p_amount),last_maintained_tick=current_tick WHERE tie_id=p_id;
 END IF;
 GET DIAGNOSTICS affected=ROW_COUNT;
 IF affected=0 THEN RETURN false; END IF;
 INSERT INTO echo_warehouse.events(tick,kind,box_id,tie_id,details) VALUES(current_tick,'maintenance',CASE WHEN p_kind='box' THEN p_id END,CASE WHEN p_kind='tie' THEN p_id END,jsonb_build_object('amount',p_amount));
 RETURN true;
END $$;
REVOKE ALL ON FUNCTION echo_warehouse.reinforce(text,bigint,double precision) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION echo_warehouse.reinforce(text,bigint,double precision) TO echo_warehouse_agent;