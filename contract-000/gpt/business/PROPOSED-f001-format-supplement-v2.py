#!/usr/bin/env python3
"""F-001 independent HOLD-only EPUB/PDF structural supplement v2.

Offline synthetic/review use only. This is not EPUBCheck, a PDF parser,
source authentication, a security boundary, or publication approval.
"""
import io
import json
import os
import re
import stat
import struct
import sys
import unicodedata
import zipfile
import zlib
from pathlib import PurePosixPath

MAX_FILE = 64 * 1024 * 1024
MAX_EXPANDED = 64 * 1024 * 1024
CHUNK = 65536


def read_bounded(path):
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) |
                 getattr(os, 'O_NONBLOCK', 0))
    try:
        a = os.fstat(fd)
        if not stat.S_ISREG(a.st_mode) or a.st_size > MAX_FILE:
            raise ValueError('not a bounded regular input')
        with os.fdopen(os.dup(fd), 'rb') as f:
            data = f.read(MAX_FILE + 1)
        b = os.fstat(fd)
        fields = lambda x: (x.st_dev, x.st_ino, x.st_size, x.st_mtime_ns, x.st_ctime_ns)
        if len(data) != a.st_size or fields(a) != fields(b):
            raise ValueError('input changed or exceeded bound')
        return data
    finally:
        os.close(fd)


def safe_name(name):
    return (bool(name) and not name.startswith('/') and '\\' not in name and
            '\x00' not in name and not PurePosixPath(name).is_absolute() and
            all(p not in ('', '.', '..') for p in name.rstrip('/').split('/')))


def deflate_declared_size(data, info):
    """Independently count raw DEFLATE output, including beyond false ZIP sizes."""
    pos = info.header_offset
    if pos < 0 or data[pos:pos + 4] != b'PK\x03\x04' or pos + 30 > len(data):
        raise ValueError('bad local header')
    name_len, extra_len = struct.unpack_from('<HH', data, pos + 26)
    start = pos + 30 + name_len + extra_len
    end = start + info.compress_size
    if end > len(data):
        raise ValueError('compressed member extends beyond archive')
    if info.compress_type == zipfile.ZIP_STORED:
        if info.compress_size != info.file_size:
            raise ValueError('STORED member size disagreement')
        return
    if info.compress_type != zipfile.ZIP_DEFLATED:
        raise ValueError('unsupported EPUB compression')
    decoder = zlib.decompressobj(-15)
    expanded = 0
    for i in range(start, end, CHUNK):
        part = decoder.decompress(data[i:min(end, i + CHUNK)],
                                  info.file_size - expanded + 1)
        expanded += len(part)
        if expanded > info.file_size or decoder.unconsumed_tail:
            raise ValueError('hidden DEFLATE expansion beyond declared size')
    if expanded != info.file_size or not decoder.eof or decoder.unused_data:
        raise ValueError('DEFLATE length/stream mismatch')


def check_epub(data):
    if not data.startswith(b'PK\x03\x04'):
        raise ValueError('EPUB ZIP has prefix or lacks local header')
    eocd = data.rfind(b'PK\x05\x06')
    if eocd < 0 or eocd + 22 > len(data):
        raise ValueError('missing ZIP end-of-central-directory')
    comment_len = struct.unpack_from('<H', data, eocd + 20)[0]
    if eocd + 22 + comment_len != len(data):
        raise ValueError('bytes after ZIP end-of-central-directory')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        if not infos or infos[0].filename != 'mimetype':
            raise ValueError('EPUB first member is not mimetype')
        seen = set()
        total = 0
        for info in infos:
            name = info.filename
            if not safe_name(name):
                raise ValueError('unsafe EPUB member name')
            key = unicodedata.normalize('NFC', name).casefold()
            if key in seen:
                raise ValueError('NFC/casefold-colliding EPUB members')
            seen.add(key)
            if info.flag_bits & 1:
                raise ValueError('encrypted EPUB member')
            if info.create_system == 3 and stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK:
                raise ValueError('ZIP symlink member')
            total += info.file_size
            if total > MAX_EXPANDED:
                raise ValueError('expanded EPUB budget exceeded')
            deflate_declared_size(data, info)
            count = 0
            with archive.open(info) as stream:
                while True:
                    chunk = stream.read(min(CHUNK, info.file_size - count + 1))
                    if not chunk:
                        break
                    count += len(chunk)
                    if count > info.file_size:
                        raise ValueError('ZIP member expanded beyond declared size')
            if count != info.file_size:
                raise ValueError('ZIP member size mismatch')
        return {'members_checked': len(infos), 'expanded_bytes': total,
                'check_level': 'bounded_zip_structure_and_crc_not_epub_conformance'}


def check_pdf(data):
    if not re.match(rb'%PDF-[12]\.[0-9]', data[:8]):
        raise ValueError('PDF header missing')
    m = re.search(rb'startxref\s+(\d+)\s+%%EOF[\x00\x09\x0a\x0c\x0d\x20]{0,64}\Z', data[-2048:])
    if not m:
        raise ValueError('PDF tail shape missing')
    offset = int(m.group(1))
    if offset >= len(data) or not (data[offset:offset + 4] == b'xref' or
        (re.match(rb'\d+\s+\d+\s+obj\b', data[offset:offset + 256]) and
         b'/XRef' in data[offset:offset + 256])):
        raise ValueError('PDF startxref pointer shape invalid')
    for pattern in (rb'(?m)^\s*\d+\s+\d+\s+obj\b', rb'/Type\s*/Catalog\b',
                    rb'/Type\s*/Pages\b', rb'/Type\s*/Page\b',
                    rb'/Root\s+\d+\s+\d+\s+R\b'):
        if not re.search(pattern, data):
            raise ValueError('PDF minimal marker missing')
    return {'check_level': 'pdf_marker_heuristic_not_object_graph_validation',
            'startxref': offset}


def check_package(epub_path, pdf_path):
    issues, observations = [], {}
    for label, path, checker in (('epub', epub_path, check_epub),
                                  ('pdf', pdf_path, check_pdf)):
        try:
            observations[label] = checker(read_bounded(path))
        except (OSError, ValueError, TypeError, OverflowError, zipfile.BadZipFile,
                NotImplementedError, EOFError, RuntimeError, zlib.error) as exc:
            issues.append(label + ': ' + str(exc))
    return {'schema': 'f001-format-supplement/v2',
            'supplement': 'PASS' if not issues else 'FAIL',
            'release': 'HOLD', 'readiness': 'BLOCKED',
            'publication_authorization': 'ABSENT',
            'full_conformance_verified': False,
            'issues': issues, 'observations': observations}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: supplement-v2.py BOOK.epub BOOK.pdf')
    result = check_package(sys.argv[1], sys.argv[2])
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result['supplement'] == 'PASS' else 1)
