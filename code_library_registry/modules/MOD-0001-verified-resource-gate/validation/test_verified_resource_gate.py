import unittest

from verified_resource_gate import ResourceSpec, VerifiedResourceGate


def make_gate():
    return VerifiedResourceGate(
        actor_id="builder",
        target_id="workspace",
        resources=(
            ResourceSpec("alpha", "cache", 0),
            ResourceSpec("beta", "index", 1),
        ),
    )


class VerifiedResourceGateTests(unittest.TestCase):
    def test_staged_run_is_valid_and_idempotent(self):
        gate = make_gate()
        self.assertFalse(gate.validate())
        first = gate.run()
        second = gate.run()
        self.assertEqual(first, second)
        self.assertTrue(first["state"]["verified"])
        self.assertTrue(first["state"]["storage_unlocked"])
        self.assertEqual(set(first["resources"]), {"alpha", "beta"})

    def test_order_and_identity_are_enforced(self):
        gate = make_gate()
        with self.assertRaises(PermissionError):
            gate.grant_creation(actor="builder")
        with self.assertRaises(PermissionError):
            make_gate().authorize_target(actor="intruder", target_id="workspace")
        with self.assertRaises(PermissionError):
            make_gate().authorize_target(actor="builder", target_id="other")

    def test_layout_tampering_revokes_access(self):
        gate = make_gate()
        gate.run()
        gate.resources["alpha"]["kind"] = "changed"
        self.assertFalse(gate.validate())
        self.assertFalse(gate.storage_unlocked)
        with self.assertRaises(PermissionError):
            gate.read_storage("beta", actor="builder")

    def test_snapshots_and_storage_are_detached(self):
        gate = make_gate()
        snapshot = gate.run()
        snapshot["resources"]["alpha"]["kind"] = "external-change"
        self.assertEqual(gate.resources["alpha"]["kind"], "cache")
        value = gate.read_storage("alpha", actor="builder")
        value["external"] = True
        self.assertEqual(gate.resources["alpha"]["storage"], {})

    def test_duplicate_resource_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            VerifiedResourceGate(
                actor_id="builder",
                target_id="workspace",
                resources=(
                    ResourceSpec("same", "cache", 0),
                    ResourceSpec("same", "index", 1),
                ),
            )


if __name__ == "__main__":
    unittest.main()
