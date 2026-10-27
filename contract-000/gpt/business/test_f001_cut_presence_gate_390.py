import csv
import tempfile
import unittest
import zipfile
from pathlib import Path
from f001_cut_presence_gate_390 import inspect, normalize

class CutGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.csv = self.root / 'claims.csv'
        self.epub = self.root / 'review.epub'

    def fixture(self, status='cut', sentence='This claim proves everything.', body='This claim proves everything.', extra=None):
        with self.csv.open('w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['sentence','status']); w.writeheader(); w.writerow({'sentence':sentence,'status':status})
        with zipfile.ZipFile(self.epub, 'w') as z:
            z.writestr('EPUB/chapter.xhtml', f'<html xmlns="http://www.w3.org/1999/xhtml"><body><p>{body}</p></body></html>')
            if extra:
                z.writestr(extra[0], extra[1])

    def test_cut_still_present_is_hold(self):
        self.fixture(); self.assertFalse(inspect(self.csv,self.epub)[0])
    def test_cut_absent_is_epub_only_pass(self):
        self.fixture(body='Unrelated manuscript content.'); self.assertTrue(inspect(self.csv,self.epub)[0])
    def test_open_status_is_hold(self):
        self.fixture(status=''); self.assertFalse(inspect(self.csv,self.epub)[0])
    def test_unicode_format_invisible(self):
        self.fixture(body='This claim pro\u200bves everything.'); self.assertFalse(inspect(self.csv,self.epub)[0])
    def test_missing_epub_is_hold(self):
        self.fixture(); self.epub.unlink(); self.assertFalse(inspect(self.csv,self.epub)[0])
    def test_empty_cut_sentence_is_hold(self):
        self.fixture(sentence=''); self.assertFalse(inspect(self.csv,self.epub)[0])
    def test_unsafe_member_is_hold(self):
        self.fixture(extra=('../escape.xhtml','<html/>')); self.assertFalse(inspect(self.csv,self.epub)[0])
    def test_malformed_xhtml_is_hold(self):
        self.fixture(extra=('EPUB/bad.xhtml','<html>')); self.assertFalse(inspect(self.csv,self.epub)[0])
    def test_no_xhtml_is_hold(self):
        self.fixture(); self.epub.unlink()
        with zipfile.ZipFile(self.epub,'w') as z:z.writestr('mimetype','application/epub+zip')
        self.assertFalse(inspect(self.csv,self.epub)[0])
    def test_normalization(self):
        self.assertEqual(normalize('  A\u200b  B\tC '),'a b c')

if __name__=='__main__':unittest.main()
