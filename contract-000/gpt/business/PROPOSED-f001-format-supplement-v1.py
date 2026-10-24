#!/usr/bin/env python3
"""F-001: independent, HOLD-only EPUB/PDF structural supplement.

Checks *all* EPUB ZIP member CRCs and collision/symlink hazards; checks
minimal PDF object markers. This is not a full format parser or release gate.
Never extracts ZIP files, mutates input, publishes, or contacts a network.
"""
import io
import json
import os
import re
import stat
import sys
import zipfile
from pathlib import PurePosixPath

MAX_FILE = 64 * 1024 * 1024
MAX_EXPANDED = 64 * 1024 * 1024
CHUNK = 65536
O_NOFOLLOW = getattr(os, 'O_NOFOLLOW', 0)
O_NONBLOCK = getattr(os, 'O_NONBLOCK', 0)


def read_bounded(path, max_size=MAX_FILE):
    fd = os.open(path, os.O_RDONLY | O_NOFOLLOW | O_NONBLOCK)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size > max_size:
            raise ValueError('input is not a bounded regular file')
        with os.fdopen(os.dup(fd), 'rb') as f:
            data = f.read(max_size + 1)
        after = os.fstat(fd)
        witness = lambda st: (st.st_dev, st.st_ino, st.st_size,
                              st.st_mtime_ns, st.st_ctime_ns)
        if len(data) > max_size or len(data) != before.st_size or witness(before) != witness(after):
            raise ValueError('input changed during read or exceeded bound')
        return data
    finally:
        os.close(fd)


def safe_zip_name(name):
    if not name or name.startswith('/') or '\\' in name or '\x00' in name:
        return False
    return not PurePosixPath(name).is_absolute() and all(
        component not in ('.', '..', '') for component in name.rstrip('/').split('/'))


def check_epub_supplement(data):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        if not infos:
            raise ValueError('empty EPUB ZIP')
        seen = set()
        total = 0
        for info in infos:
            name = info.filename
            if not safe_zip_name(name):
                raise ValueError('unsafe EPUB member path')
            key = name.casefold()
            if key in seen:
                raise ValueError('casefold-colliding EPUB members')
            seen.add(key)
            if info.flag_bits & 1:
                raise ValueError('encrypted EPUB member')
            if info.create_system == 3 and stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK:
                raise ValueError('Unix symlink EPUB member')
            total += info.file_size
            if total > MAX_EXPANDED:
                raise ValueError('expanded EPUB budget exceeded')
            size = 0
            # Opening every member forces zipfile to check CRC, even unused cover assets.
            with archive.open(info) as member:
                while True:
                    chunk = member.read(min(CHUNK, info.file_size - size + 1))
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > info.file_size or size > MAX_EXPANDED:
                        raise ValueError('member expanded beyond declared bound')
            if size != info.file_size:
                raise ValueError('member size mismatch')
        return {'members_crc_checked': len(infos), 'expanded_bytes': total}


def check_pdf_supplement(data):
    if not re.match(rb'%PDF-[12]\.[0-9]', data[:8]):
        raise ValueError('PDF header missing')
    # Tolerate up to 64 trailing NUL/ASCII whitespace bytes after EOF.
    tail = data[-2048:]
    match = re.search(rb'startxref\s+(\d+)\s+%%EOF[\x00\x09\x0a\x0c\x0d\x20]{0,64}\Z', tail)
    if not match:
        raise ValueError('PDF startxref/EOF missing')
    offset = int(match.group(1))
    if offset >= len(data) or not (
        data[offset:offset+4] == b'xref' or
        (re.match(rb'\d+\s+\d+\s+obj\b', data[offset:offset+256])
         and b'/XRef' in data[offset:offset+256])):
        raise ValueError('PDF startxref target invalid')
    objects = re.findall(rb'(?m)^\s*\d+\s+\d+\s+obj\b', data)
    if len(objects) < 3:
        raise ValueError('PDF has too few object declarations')
    for label, pattern in (
        ('catalog', rb'/Type\s*/Catalog\b'),
        ('pages', rb'/Type\s*/Pages\b'),
        ('page', rb'/Type\s*/Page\b'),
        ('root', rb'/Root\s+\d+\s+\d+\s+R\b'),
    ):
        if not re.search(pattern, data):
            raise ValueError('PDF lacks minimal ' + label + ' marker')
    return {'object_declarations': len(objects), 'startxref': offset}


def check_package(epub_path, pdf_path):
    issues, observations = [], {}
    for label, path, checker in (
        ('epub', epub_path, check_epub_supplement),
        ('pdf', pdf_path, check_pdf_supplement),
    ):
        try:
            observations[label] = checker(read_bounded(path))
        except (OSError, ValueError, TypeError, OverflowError, zipfile.BadZipFile,
                NotImplementedError, EOFError, RuntimeError) as exc:
            issues.append(label + ': ' + str(exc))
    return {'schema': 'f001-format-supplement/v1',
            'supplement': 'PASS' if not issues else 'FAIL',
            'release': 'HOLD', 'readiness': 'BLOCKED',
            'publication_authorization': 'ABSENT',
            'full_conformance_verified': False,
            'issues': issues, 'observations': observations}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: supplement.py BOOK.epub BOOK.pdf')
    result = check_package(sys.argv[1], sys.argv[2])
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result['supplement'] == 'PASS' else 1)
