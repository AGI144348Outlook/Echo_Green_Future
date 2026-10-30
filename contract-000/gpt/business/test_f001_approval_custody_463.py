"""Synthetic-only tests; real GitHub bytes are checked separately."""
import unittest
import f001_approval_custody_463 as m


def tsv(columns, rows):
    return ("\t".join(columns) + "\n" + "\n".join("\t".join(str(r[c]) for c in columns) for r in rows) + "\n").encode()


def fixture():
    reg, loc = [], []
    for i in range(82):
        ident = f"Article {i}#S{i+1}"
        link = f"Article {i-1}#S{i}" if 1 <= i <= 10 else ""
        reg.append(dict(project="F-001", occurrence_id=ident, proposal_section="§156", short_text="sample", claude_proposed_state="proposed", same_text_as=link, editorial_approval="PROPOSED_NOT_APPROVED", publication_status=m.STATUS, tam_source_commit=m.SOURCE_COMMIT, manuscript_git_blob="a"*40))
        loc.append(dict(occurrence_id=ident, source_file=f"Article {i}", sentence_no=str(i+1), source_git_blob=f"{i:040x}", quote_match_class="LITERAL", copy_target=link, source_sentence_preview="sample"))
    rb, lb = tsv(m.REGISTER_COLS, reg), tsv(m.LOCATION_COLS, loc)
    rp, lp = m.git_blob(rb), m.git_blob(lb)
    intake = m.make_pending(rb, lb, rp, lp)
    return rb, lb, intake, rp, lp


class CustodyTests(unittest.TestCase):
    def setUp(self):
        self.r, self.l, self.i, self.rp, self.lp = fixture()

    def ok(self, r=None, l=None, i=None):
        return m.validate(self.r if r is None else r, self.l if l is None else l, self.i if i is None else i, self.rp, self.lp)

    def mutate(self, column, value, row=0):
        rows = m.parse_tsv(self.i, m.INTAKE_COLS, "test")
        rows[row][column] = value
        return tsv(m.INTAKE_COLS, rows)

    def test_positive_hold(self):
        result = self.ok()
        self.assertEqual((result["pending"], result["approved"], result["publication_authorized"]), (82, 0, False))

    def test_deterministic_intake(self):
        self.assertEqual(m.make_pending(self.r, self.l, self.rp, self.lp), self.i)

    def test_register_tamper(self):
        with self.assertRaisesRegex(ValueError, "register.*blob"):
            self.ok(r=self.r.replace(b"sample", b"altered", 1))

    def test_location_tamper(self):
        with self.assertRaisesRegex(ValueError, "location map.*blob"):
            self.ok(l=self.l.replace(b"LITERAL", b"MANUAL", 1))

    def test_forged_approval(self):
        with self.assertRaisesRegex(ValueError, "unauthorized"):
            self.ok(i=self.mutate("decision", "APPROVED_BY_TIMOTHY"))

    def test_forged_approver(self):
        with self.assertRaisesRegex(ValueError, "unauthorized"):
            self.ok(i=self.mutate("approved_by", "Timothy"))

    def test_forged_evidence(self):
        with self.assertRaisesRegex(ValueError, "unauthorized"):
            self.ok(i=self.mutate("decision_evidence", "https://example.org/fake"))

    def test_replacement(self):
        with self.assertRaisesRegex(ValueError, "unauthorized"):
            self.ok(i=self.mutate("replacement_text", "unreviewed replacement"))

    def test_release(self):
        with self.assertRaisesRegex(ValueError, "unauthorized"):
            self.ok(i=self.mutate("release_authorized", "true"))

    def test_missing_id(self):
        rows = m.parse_tsv(self.i, m.INTAKE_COLS, "test")[:-1]
        with self.assertRaisesRegex(ValueError, "82"):
            self.ok(i=tsv(m.INTAKE_COLS, rows))

    def test_duplicate_id(self):
        with self.assertRaisesRegex(ValueError, "source binding"):
            self.ok(i=self.mutate("occurrence_id", "Article 0#S1", 1))

    def test_wrong_source_blob(self):
        with self.assertRaisesRegex(ValueError, "source binding"):
            self.ok(i=self.mutate("source_git_blob", "f"*40))

    def test_wrong_register_pin(self):
        with self.assertRaisesRegex(ValueError, "source binding"):
            self.ok(i=self.mutate("proposal_register_blob", "f"*40))

    def test_wrong_location_pin(self):
        with self.assertRaisesRegex(ValueError, "source binding"):
            self.ok(i=self.mutate("location_map_blob", "f"*40))

    def test_wrong_project(self):
        with self.assertRaisesRegex(ValueError, "source binding"):
            self.ok(i=self.mutate("project", "F-002"))

    def test_extra_column(self):
        with self.assertRaisesRegex(ValueError, "header"):
            self.ok(i=self.i.replace(b"release_authorized\n", b"release_authorized\textra\n", 1))

    def test_crlf(self):
        with self.assertRaisesRegex(ValueError, "noncanonical"):
            self.ok(i=self.i.replace(b"\n", b"\r\n"))

    def test_no_final_lf(self):
        with self.assertRaisesRegex(ValueError, "noncanonical"):
            self.ok(i=self.i[:-1])

    def test_invalid_utf8(self):
        with self.assertRaisesRegex(ValueError, "invalid UTF-8"):
            self.ok(i=self.i.replace(b"PENDING", b"\xffENDING", 1))

    def test_empty_source(self):
        with self.assertRaisesRegex(ValueError, "register.*blob"):
            self.ok(r=b"")

    def test_bad_duplicate_link_count(self):
        rows = m.parse_tsv(self.r, m.REGISTER_COLS, "test")
        rows[1]["same_text_as"] = ""
        r = tsv(m.REGISTER_COLS, rows)
        newpin = m.git_blob(r)
        intake_rows = m.parse_tsv(self.i, m.INTAKE_COLS, "test")
        for row in intake_rows:
            row["proposal_register_blob"] = newpin
        i = tsv(m.INTAKE_COLS, intake_rows)
        with self.assertRaisesRegex(ValueError, "copy link mismatch"):
            m.validate(r, self.l, i, newpin, self.lp)


if __name__ == "__main__":
    unittest.main(verbosity=2)
