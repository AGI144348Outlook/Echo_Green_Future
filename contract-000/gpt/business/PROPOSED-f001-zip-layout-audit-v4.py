"""F-001 candidate: conservative, read-only ZIP32/EPUB layout preflight v4.

HOLD-only. Not EPUBCheck, not an authenticity, accessibility or release check.
Strict policy: no ZIP extras/comments; exact DEFLATE EOF; portable names.
Compatibility/security correction: allow ZIP compressor-level flag bits 1-2;
require STORED size equality and reject non-UTF8 high-bit member names.
v4: bounded per-path ancestor-prefix check replaces quadratic all-pairs scan.
May reject legitimate EPUB metadata. Requires independent source pins and full EPUB/PDF checks.
"""
import hashlib
import json
import os
import stat
import struct
import sys
import unicodedata
import zipfile
import zlib
from io import BytesIO

MAX_ARCHIVE = 64 * 1024 * 1024
MAX_UNCOMPRESSED = 64 * 1024 * 1024
MIME = b'application/epub+zip'
EOCD = b'PK\x05\x06'
CENTRAL = b'PK\x01\x02'
LOCAL = b'PK\x03\x04'
DESCRIPTOR = b'PK\x07\x08'


def _fail(reason):
    raise ValueError(reason)


def _name(raw, flags):
    try:
        name = raw.decode('utf-8' if flags & 0x800 else 'cp437')
    except UnicodeDecodeError:
        _fail('invalid filename encoding')
    if not name or '\x00' in name or '\\' in name or name.startswith('/'):
        _fail('unsafe filename')
    if any(part in ('', '.', '..') for part in name.rstrip('/').split('/')):
        _fail('unsafe filename component')
    return name


def audit_bytes(data):
    if not isinstance(data, bytes) or len(data) > MAX_ARCHIVE or len(data) < 22:
        _fail('archive size invalid or over bound')
    # Only an EOCD that ends at the actual end is acceptable.
    candidates = []
    scan_start = max(0, len(data) - 22 - 65535)
    pos = data.find(EOCD, scan_start)
    while pos >= 0:
        if pos + 22 <= len(data):
            comment_len = struct.unpack_from('<H', data, pos + 20)[0]
            if pos + 22 + comment_len == len(data):
                candidates.append(pos)
        pos = data.find(EOCD, pos + 1)
    if len(candidates) != 1:
        _fail('missing or ambiguous end-of-central-directory')
    eocd = candidates[0]
    if eocd + 22 != len(data):
        _fail('ZIP archive comment forbidden by strict policy')
    (_, disk, cd_disk, disk_entries, total_entries, cd_size, cd_offset, _) = struct.unpack_from('<IHHHHIIH', data, eocd)
    if disk or cd_disk or disk_entries != total_entries or not total_entries:
        _fail('multidisk or empty ZIP unsupported')
    if total_entries == 0xffff or cd_size == 0xffffffff or cd_offset == 0xffffffff:
        _fail('ZIP64 unsupported')
    if cd_offset + cd_size != eocd:
        _fail('unaccounted bytes between central directory and EOCD')
    if cd_offset >= eocd:
        _fail('invalid central directory offset')
    entries = []
    cursor = cd_offset
    total_uncompressed = 0
    normalized = set()
    for _ in range(total_entries):
        if cursor + 46 > eocd or data[cursor:cursor+4] != CENTRAL:
            _fail('central directory entry invalid')
        fields = struct.unpack_from('<IHHHHHHIIIHHHHHII', data, cursor)
        (_, made, needed, flags, method, mt, md, crc, comp, uncomp,
         nlen, xlen, clen, disk_start, internal, external, localoff) = fields
        if disk_start or comp == 0xffffffff or uncomp == 0xffffffff or localoff == 0xffffffff:
            _fail('ZIP64 or multidisk member unsupported')
        if flags & ~(0x800 | 0x08 | 0x06) or method not in (0, 8):
            _fail('unsupported ZIP flags or compression')
        if uncomp > MAX_UNCOMPRESSED or total_uncompressed + uncomp > MAX_UNCOMPRESSED:
            _fail('uncompressed size exceeds bound')
        total_uncompressed += uncomp
        end = cursor + 46 + nlen + xlen + clen
        if end > eocd:
            _fail('central directory entry truncated')
        raw_name = data[cursor+46:cursor+46+nlen]
        if any(byte >= 0x80 for byte in raw_name) and not flags & 0x800:
            _fail('non-ASCII EPUB filename requires UTF-8 flag')
        name = _name(raw_name, flags)
        if xlen or clen:
            _fail('central extra or member comment forbidden by strict policy')
        if any(ord(c) < 32 or ord(c) == 127 or c in ':*?"<>|' for c in name) or name.rstrip('/').endswith('.'):
            _fail('unsafe portable EPUB filename')
        norm = unicodedata.normalize('NFC', name.rstrip('/')).casefold()
        if norm in normalized:
            _fail('normalized file/directory collision')
        normalized.add(norm)
        if stat.S_IFMT(external >> 16) == stat.S_IFLNK:
            _fail('symbolic link member unsupported')
        entries.append(dict(name=name, raw_name=raw_name, flags=flags, method=method,
                            crc=crc, comp=comp, uncomp=uncomp, offset=localoff,
                            nlen=nlen, xlen=xlen))
        cursor = end
    if cursor != eocd:
        _fail('unaccounted bytes inside central directory')
    # A file cannot be an ancestor of another member. Each path is
    # normalized once; compare only proper slash-delimited prefixes against
    # file names. This avoids the quadratic all-pairs scan in v3.
    file_names = {unicodedata.normalize('NFC', entry['name']).casefold()
                  for entry in entries if not entry['name'].endswith('/')}
    for entry in entries:
        norm_name = unicodedata.normalize('NFC', entry['name'].rstrip('/')).casefold()
        slash = norm_name.find('/')
        while slash != -1:
            if norm_name[:slash] in file_names:
                _fail('file used as directory ancestor')
            slash = norm_name.find('/', slash + 1)
    ordered = sorted(entries, key=lambda e: e['offset'])
    if ordered[0]['name'] != 'mimetype' or ordered[0]['offset'] != 0:
        _fail('OCF mimetype must be first local member at offset zero')
    next_offset = 0
    for i, entry in enumerate(ordered):
        offset = entry['offset']
        if offset != next_offset:
            _fail('unaccounted ZIP gap or overlapping local member')
        if offset + 30 > cd_offset or data[offset:offset+4] != LOCAL:
            _fail('invalid local header')
        (_, ver, flags, method, mt, md, crc, comp, uncomp, nlen, xlen) = struct.unpack_from('<IHHHHHIIIHH', data, offset)
        if flags != entry['flags'] or method != entry['method']:
            _fail('local and central header disagree')
        start = offset + 30
        data_start = start + nlen + xlen
        if xlen:
            _fail('local extra forbidden by strict policy')
        data_end = data_start + entry['comp']
        if data_end > cd_offset or data[start:start+nlen] != entry['raw_name']:
            _fail('local filename or compressed extent invalid')
        if not flags & 0x08 and (crc, comp, uncomp) != (entry['crc'], entry['comp'], entry['uncomp']):
            _fail('local and central sizes or CRC disagree')
        if flags & 0x08 and any(a not in (0, b) for a,b in zip((crc, comp, uncomp),
                                    (entry['crc'], entry['comp'], entry['uncomp']))):
            _fail('data descriptor local fields inconsistent')
        if method == zipfile.ZIP_STORED and entry['comp'] != entry['uncomp']:
            _fail('STORED compressed and uncompressed sizes differ')
        if method == zipfile.ZIP_DEFLATED:
            inflater = zlib.decompressobj(-15)
            inflated = inflater.decompress(data[data_start:data_end], entry['uncomp'] + 1)
            if (not inflater.eof or inflater.unused_data or inflater.unconsumed_tail
                    or len(inflated) != entry['uncomp']):
                _fail('raw DEFLATE stream does not exactly fill declared extent')
        next_offset = data_end
        if flags & 0x08:
            if data[next_offset:next_offset+4] == DESCRIPTOR:
                next_offset += 4
            if next_offset + 12 > cd_offset:
                _fail('data descriptor truncated')
            actual = struct.unpack_from('<III', data, next_offset)
            if actual != (entry['crc'], entry['comp'], entry['uncomp']):
                _fail('data descriptor mismatch')
            next_offset += 12
        if i == 0:
            if method != zipfile.ZIP_STORED or xlen or nlen != 8:
                _fail('OCF mimetype header must be uncompressed and without extra')
            if entry['uncomp'] != len(MIME) or entry['comp'] != len(MIME) or data[data_start:data_end] != MIME:
                _fail('OCF mimetype content invalid')
    if next_offset != cd_offset:
        _fail('unaccounted ZIP bytes before central directory')
    try:
        with zipfile.ZipFile(BytesIO(data)) as archive:
            if archive.testzip() is not None:
                _fail('ZIP member CRC invalid')
    except (zipfile.BadZipFile, RuntimeError, EOFError, OverflowError) as exc:
        _fail('ZIP reader rejected archive: ' + type(exc).__name__)
    return {'members': len(entries), 'zip32_layout_tiled': True,
            'mimetype_rule': True, 'member_crc_checked': True}


def check_package_bytes(data):
    try:
        observations = audit_bytes(data)
        issues = []
    except (ValueError, OSError, struct.error, UnicodeError, zlib.error) as exc:
        observations, issues = {}, [str(exc)]
    return {'schema': 'f001-zip-layout-audit/v4',
            'layout': 'PASS' if not issues else 'FAIL',
            'release': 'HOLD', 'readiness': 'BLOCKED',
            'publication_authorization': 'ABSENT',
            'complete_epub_conformance_verified': False,
            'sha256': hashlib.sha256(data).hexdigest(),
            'issues': issues, 'observations': observations}


def _read_regular(path):
    flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_NOFOLLOW', 0)
    fd = os.open(path, flags)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_ARCHIVE:
            _fail('input not a bounded regular file')
        with os.fdopen(os.dup(fd), 'rb') as f:
            data = f.read(MAX_ARCHIVE + 1)
        if len(data) > MAX_ARCHIVE:
            _fail('input exceeds archive bound')
        return data
    finally:
        os.close(fd)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: PROPOSED-f001-zip-layout-audit-v4.py BOOK.epub')
    try:
        result = check_package_bytes(_read_regular(sys.argv[1]))
    except (OSError, ValueError) as exc:
        result = {'schema': 'f001-zip-layout-audit/v3', 'layout': 'FAIL',
                  'release': 'HOLD', 'readiness': 'BLOCKED',
                  'publication_authorization': 'ABSENT',
                  'issues': [str(exc)]}
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(3 if result['layout'] == 'PASS' else 1)  # HOLD is never exit-0 authorization
