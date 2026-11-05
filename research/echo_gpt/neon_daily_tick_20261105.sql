-- UTC-day idempotency for scheduled ticks
CREATE TABLE IF NOT EXISTS echo_warehouse.daily_ticks (day_utc date PRIMARY KEY,tick bigint NOT NULL,executed_at timestamptz NOT NULL DEFAULT now());
CREATE OR REPLACE FUNCTION echo_warehouse.apply_daily_entropy_tick() RETURNS bigint LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,echo_warehouse AS $$ DECLARE d date; t bigint; BEGIN d:=(now() AT TIME ZONE 'UTC')::date; PERFORM pg_advisory_xact_lock(20261105,340); SELECT tick INTO t FROM echo_warehouse.daily_ticks WHERE day_utc=d; IF FOUND THEN RETURN t; END IF; t:=echo_warehouse.apply_entropy_tick(); INSERT INTO echo_warehouse.daily_ticks(day_utc,tick) VALUES(d,t); RETURN t; END $$;
REVOKE ALL ON FUNCTION echo_warehouse.apply_daily_entropy_tick() FROM PUBLIC;
REVOKE ALL ON FUNCTION echo_warehouse.apply_entropy_tick() FROM echo_entropy_scheduler;
GRANT EXECUTE ON FUNCTION echo_warehouse.apply_daily_entropy_tick() TO echo_entropy_scheduler;
