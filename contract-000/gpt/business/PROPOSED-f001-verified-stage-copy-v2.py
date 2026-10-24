"""F-001 proposal: descriptor-held non-clobber copy with bounded SHA checks.

Cooperative offline integrity only. Caller supplies pins; no signature, sandbox,
subprocess containment, publication authorization, or same-UID immutability.
Destination parent must be a newly created, caller-controlled 0700 directory.
"""
import hashlib
import os
from pathlib import Path
import stat

CHUNK = 65536
MAX_BYTES = 120 * 1024 * 1024
O_NOFOLLOW = getattr(os, 'O_NOFOLLOW', 0)
O_NONBLOCK = getattr(os, 'O_NONBLOCK', 0)
O_DIRECTORY = getattr(os, 'O_DIRECTORY', 0)

def _witness(s):
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)

def _sha_ok(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)

def digest_regular(path, *, limit=MAX_BYTES):
    """Read regular file with O_NOFOLLOW; reject size/metadata changes."""
    fd = os.open(path, os.O_RDONLY | O_NOFOLLOW | O_NONBLOCK)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
            raise ValueError('not bounded regular file')
        h, count = hashlib.sha256(), 0
        while True:
            block = os.read(fd, CHUNK)
            if not block: break
            count += len(block)
            if count > limit: raise ValueError('stream exceeds limit')
            h.update(block)
        after = os.fstat(fd)
        if _witness(before) != _witness(after) or count != after.st_size:
            raise ValueError('file changed during verification')
        return h.hexdigest(), count
    finally:
        os.close(fd)

def copy_verified(source, destination, expected_sha256, expected_size, *, limit=MAX_BYTES):
    """Copy held source FD into exclusive destination and verify bytes.

    The destination parent must be private (0700, owned by this process uid).
    A failed O_EXCL never unlinks an existing file. fchmod targets the held
    destination FD, never a pathname. Cleanup unlinks only the inode created
    by this invocation, under the held parent directory FD.
    """
    if type(expected_size) is not int or expected_size < 0 or expected_size > limit:
        raise ValueError('invalid expected size')
    if not _sha_ok(expected_sha256):
        raise ValueError('invalid SHA-256')
    dest = Path(destination)
    if dest.name in ('', '.', '..'):
        raise ValueError('invalid destination label')
    parent_fd = os.open(dest.parent, os.O_RDONLY | O_DIRECTORY | O_NOFOLLOW)
    try:
        parent = os.fstat(parent_fd)
        if not stat.S_ISDIR(parent.st_mode) or parent.st_uid != os.getuid() or parent.st_mode & 0o077:
            raise ValueError('destination parent not private')
        source_fd = os.open(source, os.O_RDONLY | O_NOFOLLOW | O_NONBLOCK)
        try:
            before = os.fstat(source_fd)
            if not stat.S_ISREG(before.st_mode) or before.st_size != expected_size:
                raise ValueError('snapshot size/type mismatch')
            # Open outside the cleanup try: failure to create is not ownership.
            out_fd = os.open(dest.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | O_NOFOLLOW,
                             0o600, dir_fd=parent_fd)
            created = os.fstat(out_fd)
            try:
                h, count = hashlib.sha256(), 0
                with os.fdopen(out_fd, 'wb') as out:
                    while True:
                        block = os.read(source_fd, CHUNK)
                        if not block: break
                        count += len(block)
                        if count > limit or count > expected_size:
                            raise ValueError('snapshot exceeds bound')
                        h.update(block)
                        out.write(block)
                    out.flush()
                    os.fsync(out.fileno())
                    after = os.fstat(source_fd)
                    if _witness(before) != _witness(after) or count != expected_size or h.hexdigest() != expected_sha256:
                        raise ValueError('snapshot changed or digest mismatch')
                    # Mode change acts on the held inode, even if the path swaps.
                    os.fchmod(out.fileno(), 0o400)
                    os.fsync(out.fileno())
                observed_sha, observed_size = digest_regular(dest, limit=limit)
                if (observed_sha, observed_size) != (expected_sha256, expected_size):
                    raise ValueError('staged output digest mismatch')
                return {'sha256': observed_sha, 'size': observed_size}
            except BaseException:
                # A same-UID attacker may swap the path: never unlink a different inode.
                try:
                    current = os.stat(dest.name, dir_fd=parent_fd, follow_symlinks=False)
                    if (current.st_dev, current.st_ino) == (created.st_dev, created.st_ino):
                        os.unlink(dest.name, dir_fd=parent_fd)
                except FileNotFoundError:
                    pass
                raise
        finally:
            os.close(source_fd)
    finally:
        os.close(parent_fd)

def verify_staged(expected_by_path, *, limit=MAX_BYTES):
    observed = {}
    for path, expected in expected_by_path.items():
        sha, size = digest_regular(path, limit=limit)
        if (sha, size) != (expected['sha256'], expected['size']):
            raise ValueError('staged file changed: ' + str(path))
        observed[str(path)] = {'sha256': sha, 'size': size}
    return observed
