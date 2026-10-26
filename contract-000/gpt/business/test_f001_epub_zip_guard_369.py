import contextlib
import io
import os
import stat
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

from f001_epub_zip_guard_369 import MIMETYPE, Reject, guard, main


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.p = Path(self.tmp.name) / 'draft.epub'

    def make(self, entries, *, first_stored=True):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(self.p, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                for n, value in entries:
                    if isinstance(n, zipfile.ZipInfo):
                        z.writestr(n, value)
                    else:
                        z.writestr(n, value, compress_type=(zipfile.ZIP_STORED if n == 'mimetype' and first_stored else zipfile.ZIP_DEFLATED))

    def good(self):
        return [('mimetype', MIMETYPE), ('META-INF/container.xml', b'<root/>'), ('OEBPS/book.opf', b'<package/>')]

    def reject(self, entries, **kw):
        self.make(entries, **kw)
        with self.assertRaises(Reject):
            guard(self.p)

    def test_accept_safe_minimal_zip_only(self):
        self.make(self.good())
        r = guard(self.p)
        self.assertEqual(r['status'], 'HOLD_PASSED_ZIP_PREFLIGHT')
        self.assertEqual(r['entries'], 3)

    def test_missing_mimetype(self):
        self.reject([('x.txt', b'a')])

    def test_late_mimetype(self):
        self.reject([('x.txt', b'a')] + self.good())

    def test_compressed_mimetype(self):
        self.reject(self.good(), first_stored=False)

    def test_wrong_mimetype(self):
        self.reject([('mimetype', b'wrong')] + self.good()[1:])

    def test_duplicate_member(self):
        self.reject(self.good() + [('OEBPS/book.opf', b'again')])

    def test_traversal(self):
        self.reject(self.good() + [('OEBPS/../secret.txt', b'x')])

    def test_absolute(self):
        self.reject(self.good() + [('/etc/passwd', b'x')])

    def test_backslash(self):
        self.reject(self.good() + [('OEBPS\\secret.txt', b'x')])

    def test_drive_path(self):
        self.reject(self.good() + [('C:/secret.txt', b'x')])

    def test_symlink_member(self):
        info = zipfile.ZipInfo('OEBPS/link')
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.reject(self.good() + [(info, b'../../outside')])

    def test_high_ratio(self):
        self.reject(self.good() + [('OEBPS/compressible.xhtml', b'Z' * 300000)])

    def test_entry_limit(self):
        self.make(self.good() + [('OEBPS/extra', b'')])
        with self.assertRaises(Reject): guard(self.p, limits={'max_entries': 3})

    def test_member_limit(self):
        self.make(self.good() + [('OEBPS/extra', b'Z' * 1024)])
        with self.assertRaises(Reject): guard(self.p, limits={'max_member_uncompressed': 1000})

    def test_total_limit(self):
        self.make(self.good() + [('OEBPS/extra', b'Z' * 1024)])
        with self.assertRaises(Reject): guard(self.p, limits={'max_total_uncompressed': 1024})

    def test_not_a_zip(self):
        self.p.write_bytes(b'not a zip')
        with self.assertRaises(Reject): guard(self.p)

    def test_symlink_input(self):
        self.make(self.good())
        link = Path(self.tmp.name) / 'linked.epub'
        link.symlink_to(self.p)
        with self.assertRaises(Reject): guard(link)

    def test_cli_reject_nonzero(self):
        self.p.write_bytes(b'bad')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['script', str(self.p)]), 2)

    def test_cli_pass_zero(self):
        self.make(self.good())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['script', str(self.p)]), 0)

    def test_invalid_limits(self):
        self.make(self.good())
        with self.assertRaises(ValueError): guard(self.p, limits={'max_entries': 0})


if __name__ == '__main__':
    unittest.main()
