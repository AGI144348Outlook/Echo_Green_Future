"""MCW client: message envelopes and a local outbox.

This module never opens a network connection and never holds credentials.
It builds envelopes; the host (bridge.js) delivers them to the endpoint the
user configures, and anything undelivered stays queued in the local NVE.
Authentication belongs to the Cloudflare gateway, not to this package.
"""
import time

SCHEMA = "mcw/0.1"


class Outbox:
    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.n = 0

    def envelope(self, kind, payload, to="eve", actor="echo"):
        self.n += 1
        return {
            "schema": SCHEMA,
            "id": f"{self.instance_id}-{int(time.time() * 1000):x}-{self.n}",
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "from": {"actor": actor, "instance": self.instance_id},
            "to": to,
            "kind": kind,
            "payload": payload,
        }
