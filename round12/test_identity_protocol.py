"""Round 12 preregistered protocol checks. Run with python -m unittest discover -s round12."""
import unittest
from identity_protocol import Actor, Envelope, IdentityProtocol

class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.p = IdentityProtocol()
        self.p.register("echo", "Echo")
        self.p.register("peer", "Peer")

    def packet(self, sender="echo", recipient="peer", claimed_sender="echo",
               context="exchange", source_ref="synthetic:test", payload="hello"):
        return Envelope(sender, recipient, context, payload, source_ref, claimed_sender)

    def test_self_other(self):
        self.assertEqual(self.p.identify("echo", "echo")["relation"], "self")
        self.assertEqual(self.p.identify("echo", "peer")["relation"], "other")

    def test_unknown(self):
        self.assertEqual(self.p.identify("echo", "missing")["relation"], "unknown")

    def test_duplicate_identity_rejected(self):
        with self.assertRaises(ValueError):
            self.p.register("echo", "Different Echo")

    def test_roles_change_identity_does_not(self):
        self.p.send(self.packet(), "echo")
        self.p.send(self.packet(sender="peer", recipient="echo", claimed_sender="peer"), "peer")
        self.assertEqual(self.p.events[0]["sender_role"], "source")
        self.assertEqual(self.p.events[1]["recipient_role"], "recipient")
        self.assertEqual(self.p.identify("echo", "echo")["relation"], "self")

    def test_spoofed_sender_rejected(self):
        with self.assertRaises(PermissionError):
            self.p.send(self.packet(claimed_sender="peer"), "echo")
        with self.assertRaises(PermissionError):
            self.p.send(self.packet(), "peer")

    def test_provenance_required(self):
        with self.assertRaises(ValueError):
            self.p.send(self.packet(source_ref=""), "echo")

    def test_bounded(self):
        with self.assertRaises(ValueError):
            self.p.send(self.packet(payload="x" * 2049), "echo")

    def test_unverified_not_canonical(self):
        self.assertEqual(self.p.send(self.packet(), "echo")["claim_status"], "unverified")

    def test_deterministic_replay(self):
        other = IdentityProtocol()
        other.register("echo", "Echo")
        other.register("peer", "Peer")
        self.p.send(self.packet(), "echo")
        other.send(self.packet(), "echo")
        self.assertEqual(self.p.transcript(), other.transcript())

    def test_no_mutation_on_rejection(self):
        with self.assertRaises(PermissionError):
            self.p.send(self.packet(), "peer")
        self.assertEqual(self.p.events, [])

if __name__ == "__main__":
    unittest.main()
