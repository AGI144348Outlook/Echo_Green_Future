"""F-001 proposal: verify copied staged bytes against independently supplied pins.

Cooperative offline integrity only. Same-UID actors can modify staged files after
verification. This helper does not authenticate pins or contain subprocesses.
"""
import hashlib
import os
from pathlib import Path
import stat

CHUNK = 65536
MAX_BYTES = 120 * 1024 * 1024


def digest_regular(path, *, limit=MAX_BYTES):
    """Return (digest, length) after bounded descriptor-based regular-file read."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
            raise ValueError('not bounded regular file')
        h = hashlib.sha256()
        count = 0
        while True:
            block = os.read(fd, CHUNK)
            if not block:
                break
            count += len(block)
            if count > limit:
                raise ValueError('stream exceeds limit')
            h.update(block)
        after = os.fstat(fd)
        witness = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        if witness(before) != witness(after) or count != after.st_size:
            raise ValueError('file changed during verification')
        return h.hexdigest(), count
    finally:
        os.close(fd)


def copy_verified(source, destination, expected_sha256, expected_size, *, limit=MAX_BYTES):
    """Copy a snapshot through a held FD; verify source, output and exact size.

    destination must be in a private newly created directory. An exception removes
    the partially written destination. The caller must not publish these bytes.
    """
    if type(expected_size) is not int or expected_size < 0 or expected_size > limit:
        raise ValueError('invalid expected size')
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64 or any(c not in '0123456789abcdef' for c in expected_sha256):
        raise ValueError('invalid SHA-256')
    source_fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    dest = Path(destination)
    try:
        before = os.fstat(source_fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size != expected_size:
            raise ValueError('snapshot size/type mismatch')
        count = 0
        h = hashlib.sha256()
        try:
            with os.fdopen(os.open(dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'wb') as out:
                while True:
                    block = os.read(source_fd, CHUNK)
                    if not block:
                        break
                    count += len(block)
                    if count > limit or count > expected_size:
                        raise ValueError('snapshot exceeds bound')
                    h.update(block)
                    out.write(block)
                out.flush()
                os.fsync(out.fileno())
            after = os.fstat(source_fd)
            witness = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
            if witness(before) != witness(after) or count != expected_size or h.hexdigest() != expected_sha256:
                raise ValueError('snapshot changed or digest mismatch')
            os.chmod(dest, 0o400)
            observed_sha, observed_size = digest_regular(dest, limit=limit)
            if (observed_sha, observed_size) != (expected_sha256, expected_size):
                raise ValueError('staged output digest mismatch')
            return {'sha256': observed_sha, 'size': observed_size}
        except Exception:
            dest.unlink(missing_ok=True)
            raise
    finally:
        os.close(source_fd)


def verify_staged(expected_by_path, *, limit=MAX_BYTES):
    """Fail closed if any staged path no longer matches its pinned bytes."""
    observed = {}
    for path, expected in expected_by_path.items():
        sha, size = digest_regular(path, limit=limit)
        if (sha, size) != (expected['sha256'], expected['size']):
            raise ValueError('staged file changed: ' + str(path))
        observed[str(path)] = {'sha256': sha, 'size': size}
    return observed
