"""F-001 research proposal: bounded, digest-pinned, fd-based input snapshots.

No production coordinator integration, source authentication or security sandbox.
All hashes MUST come from an independently reviewed manifest, not from the file itself.
Linux/POSIX semantics assumed. The returned paths live only inside the context.
"""
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
import stat
import tempfile

MAX_INPUT_BYTES = 16 * 1024 * 1024
CHUNK = 64 * 1024
LABEL = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")
HEX256 = re.compile(r"^[a-f0-9]{64}$")
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, 'O_CLOEXEC', 0)
FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | getattr(os, 'O_CLOEXEC', 0)


@dataclass(frozen=True)
class SnapshotRecord:
    path: str
    sha256: str
    size: int
    source_relative_path: str


def _relative_parts(value):
    if not isinstance(value, str) or not value or value.startswith('/') or '\\' in value or '\x00' in value:
        raise ValueError('unsafe relative path')
    parts = value.split('/')
    if any(p in ('', '.', '..') for p in parts):
        raise ValueError('unsafe relative component')
    return parts


def _open_beneath(root_fd, parts):
    opened = []
    current = root_fd
    try:
        for component in parts[:-1]:
            nxt = os.open(component, DIR_FLAGS, dir_fd=current)
            opened.append(nxt)
            current = nxt
        fd = os.open(parts[-1], FILE_FLAGS, dir_fd=current)
        return fd
    finally:
        for descriptor in reversed(opened):
            os.close(descriptor)


def _copy_pinned(fd, target, expected, max_bytes):
    before = os.fstat(fd)
    if not stat.S_ISREG(before.st_mode):
        raise ValueError('source is not a regular file')
    if before.st_size > max_bytes:
        raise ValueError('source exceeds byte bound')
    h = hashlib.sha256()
    total = 0
    with open(target, 'xb') as dest:
        os.chmod(target, 0o600)
        while True:
            chunk = os.read(fd, CHUNK)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise ValueError('stream exceeds byte bound')
            dest.write(chunk)
            h.update(chunk)
        dest.flush()
        os.fsync(dest.fileno())
    after = os.fstat(fd)
    witness = lambda st: (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
    if witness(before) != witness(after) or total != after.st_size:
        raise ValueError('source changed during snapshot')
    digest = h.hexdigest()
    if digest != expected:
        raise ValueError('source digest mismatch')
    os.chmod(target, 0o400)
    return digest, total


@contextmanager
def pinned_snapshots(source_root, items, *, max_bytes=MAX_INPUT_BYTES, _after_open=None):
    """Yield {label: SnapshotRecord} in a private staging directory.

    items maps distinct labels to (relative source path, expected SHA-256).
    Any failure discards the whole batch; never returns partial snapshots.
    _after_open is an optional test-only race-injection hook.
    """
    if not isinstance(items, dict) or not items:
        raise ValueError('nonempty mapping required')
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or max_bytes <= 0:
        raise ValueError('invalid bound')
    checked = []
    for label, pair in items.items():
        if not isinstance(label, str) or not LABEL.fullmatch(label):
            raise ValueError('invalid output label')
        if not isinstance(pair, (tuple, list)) or len(pair) != 2:
            raise ValueError('expected (path, digest)')
        path, digest = pair
        parts = _relative_parts(path)
        if not isinstance(digest, str) or not HEX256.fullmatch(digest):
            raise ValueError('invalid expected digest')
        checked.append((label, path, parts, digest))
    root_fd = os.open(os.fspath(source_root), DIR_FLAGS)
    try:
        with tempfile.TemporaryDirectory(prefix='f001-pinned-') as staging:
            result = {}
            for label, relative, parts, expected in checked:
                fd = _open_beneath(root_fd, parts)
                try:
                    if _after_open is not None:
                        _after_open(label, relative, fd)
                    dest = str(Path(staging) / label)
                    digest, size = _copy_pinned(fd, dest, expected, max_bytes)
                    result[label] = SnapshotRecord(dest, digest, size, relative)
                finally:
                    os.close(fd)
            yield result
    finally:
        os.close(root_fd)
