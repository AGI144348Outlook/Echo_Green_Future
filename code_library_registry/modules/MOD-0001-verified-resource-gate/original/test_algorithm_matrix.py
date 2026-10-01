import unittest
from algorithm_matrix import AlgorithmMatrixRuntime

class BootTests(unittest.TestCase):
    def test_boot_and_repeat(self):
        r = AlgorithmMatrixRuntime()
        self.assertFalse(r.alg_002())
        s = r.run_boot_handshake()
        self.assertTrue(s["system_state"]["alg_002_status"])
        self.assertTrue(s["system_state"]["storage_unlocked"])
        self.assertEqual(len(s["sub_matrices"]), 27)
        self.assertEqual(s["sub_matrices"]["extended:4"]["glyph"], "ך")
        self.assertEqual({v["glyph"] for v in s["sub_matrices"].values() if v["group"] == "extended"}, set("ךםןףץ"))
        self.assertFalse(s["primary"]["matrix_data"][0]["executable"])
        self.assertEqual(s, r.run_boot_handshake())
        s["primary"]["status"] = "CORRUPTED"
        self.assertEqual(r.primary["status"], "UNLOCKED")

    def test_denied_identity_scope_and_order(self):
        for action in (
            lambda r: r.alg_001(actor="other"),
            lambda r: r.alg_001(target="other"),
            lambda r: r.alg_001(slot=(0, 1)),
            lambda r: r.alg_003(),
            lambda r: r.alg_004(),
            lambda r: r.alg_005(),
            lambda r: r.alg_006(),
        ):
            r = AlgorithmMatrixRuntime()
            with self.assertRaises(PermissionError):
                action(r)
            self.assertFalse(r.storage_unlocked)

    def test_tampering_revokes_access(self):
        for change in (
            lambda r: r.sub_matrices.pop("standard:0"),
            lambda r: r.sub_matrices["extended:4"].update(glyph="ל"),
        ):
            r = AlgorithmMatrixRuntime()
            r.run_boot_handshake()
            change(r)
            self.assertFalse(r.alg_002())
            with self.assertRaises(PermissionError):
                r.storage("standard:1")

