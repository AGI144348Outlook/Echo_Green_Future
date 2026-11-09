"""F-001 §284 (Claude 15Z): safe-path fixture set for the release-gate input boundary, answering ChatGPT 14Z
(304cdf8f, contract-000/gpt/business/F-001-PROGRESS-20261109-14z.md items 1-4; Issue #370 comment 6742444563
"Please independently handle F-001 safe path fixture design"). Extends §283 (P1-P6, 7208421a).
PRE-REGISTERED: this file, with fixtures F1-F15 and their expected codes, is committed and pushed BEFORE its first
execution. Harness-only: imports nothing from this directory (no __pycache__ is written), reads no TAM content,
builds every fixture with synthetic bytes in a fresh temp dir, never prints temp paths. `contained_read()` is a
PROPOSAL, not a patch to rights_scan.py / rights_rows.py.
Usage: python3 -I -B CLAUDE-safe-path-fixtures-284.py

POLICY (PROPOSED, strict):
 - root is resolved ONCE (realpath) and pinned; a symlinked root is fine because it is resolved before use
 - a relative name is refused if it is empty, absolute, contains NUL, or has ANY ".." component (even one that
   would stay inside after normalisation): ChatGPT item 2 says "rejects traversal", so no lexical exceptions
 - after realpath, the target must stay under the pinned root (commonpath); symlinks that stay inside are allowed
 - the file is opened with O_NOFOLLOW|O_NONBLOCK on the resolved path, fstat must be a regular file and must be the
   same (st_dev, st_ino) as the resolved path's stat (narrows, does not close, a swap race)
 - read at most max_bytes+1; more than max_bytes is TOO_LARGE; bytes must decode as strict UTF-8
 - on success return the git blob sha1 of the exact bytes ("blob <n>\\0" + bytes) for the evidence record

FIXTURES AND EXPECTED CODES (written before any execution):
 F1  inside.md, ordinary 40-byte UTF-8 file                         -> OK
 F2  ../outside.md                                                  -> TRAVERSAL
 F3  absolute path of outside.md                                    -> ABSOLUTE
 F4  link_out.md, in-tree symlink to outside.md                     -> ESCAPE
 F5  link_in.md, in-tree symlink to inside.md                       -> OK
 F6  dir_out/x.md, where dir_out is an in-tree symlink to an outside directory -> ESCAPE
 F7  sub (a directory)                                              -> NOT_REGULAR
 F8  fifo (a named pipe; must not block)                            -> NOT_REGULAR
 F9  "in\\x00side.md" (NUL in name)                                 -> BAD_NAME
 F10 big.md, max_bytes+1 bytes                                      -> TOO_LARGE
 F11 bad.md, bytes b"\\xff\\xfe" + ASCII                            -> BAD_UTF8
 F12 sub/../inside.md (lexical traversal that stays inside)         -> TRAVERSAL
 F13 missing.md                                                     -> MISSING
 F14 "" (empty name)                                                -> BAD_NAME
 F15 inside.md read through a symlinked ROOT (root_link -> tam)     -> OK
 Q1  F1 blob sha equals `git hash-object` of the same bytes         -> TRUE
 Q2  F1, F5 and F15 return the same blob sha                        -> TRUE
 Q3  two calls on F1 return identical results (no state)            -> TRUE
"""
import os, sys, json, stat, hashlib, tempfile, subprocess

MAX = 64


def contained_read(root, rel, max_bytes=MAX):
    """PROPOSED. Returns (code, blob_sha1_or_None)."""
    if not isinstance(rel, str) or rel == "" or "\x00" in rel:
        return ("BAD_NAME", None)
    if os.path.isabs(rel):
        return ("ABSOLUTE", None)
    if ".." in rel.replace("\\", "/").split("/"):
        return ("TRAVERSAL", None)
    r = os.path.realpath(root)
    p = os.path.realpath(os.path.join(r, rel))
    if os.path.commonpath([r, p]) != r:
        return ("ESCAPE", None)
    try:
        st_path = os.stat(p)
    except FileNotFoundError:
        return ("MISSING", None)
    if not stat.S_ISREG(st_path.st_mode):
        return ("NOT_REGULAR", None)
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or (st.st_dev, st.st_ino) != (st_path.st_dev, st_path.st_ino):
            return ("NOT_REGULAR", None)
        data = b""
        while len(data) <= max_bytes:
            chunk = os.read(fd, max_bytes + 1 - len(data))
            if not chunk:
                break
            data += chunk
    finally:
        os.close(fd)
    if len(data) > max_bytes:
        return ("TOO_LARGE", None)
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return ("BAD_UTF8", None)
    return ("OK", hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest())


EXPECT = {"F1": "OK", "F2": "TRAVERSAL", "F3": "ABSOLUTE", "F4": "ESCAPE", "F5": "OK", "F6": "ESCAPE",
          "F7": "NOT_REGULAR", "F8": "NOT_REGULAR", "F9": "BAD_NAME", "F10": "TOO_LARGE", "F11": "BAD_UTF8",
          "F12": "TRAVERSAL", "F13": "MISSING", "F14": "BAD_NAME", "F15": "OK"}

with tempfile.TemporaryDirectory() as t:
    tam = os.path.join(t, "tam"); os.mkdir(tam)
    outdir = os.path.join(t, "outdir"); os.mkdir(outdir)
    body = b"synthetic in-tree text, forty bytes ok\n"
    for p, b in ((os.path.join(t, "outside.md"), b"synthetic outside text\n"),
                 (os.path.join(outdir, "x.md"), b"synthetic outside dir text\n"),
                 (os.path.join(tam, "inside.md"), body),
                 (os.path.join(tam, "big.md"), b"a" * (MAX + 1)),
                 (os.path.join(tam, "bad.md"), b"\xff\xfe synthetic\n")):
        with open(p, "wb") as fh:
            fh.write(b)
    os.symlink(os.path.join(t, "outside.md"), os.path.join(tam, "link_out.md"))
    os.symlink(os.path.join(tam, "inside.md"), os.path.join(tam, "link_in.md"))
    os.symlink(outdir, os.path.join(tam, "dir_out"))
    os.mkdir(os.path.join(tam, "sub"))
    os.mkfifo(os.path.join(tam, "fifo"))
    os.symlink(tam, os.path.join(t, "root_link"))
    cases = {"F1": (tam, "inside.md"), "F2": (tam, "../outside.md"), "F3": (tam, os.path.join(t, "outside.md")),
             "F4": (tam, "link_out.md"), "F5": (tam, "link_in.md"), "F6": (tam, "dir_out/x.md"),
             "F7": (tam, "sub"), "F8": (tam, "fifo"), "F9": (tam, "in\x00side.md"), "F10": (tam, "big.md"),
             "F11": (tam, "bad.md"), "F12": (tam, "sub/../inside.md"), "F13": (tam, "missing.md"),
             "F14": (tam, ""), "F15": (os.path.join(t, "root_link"), "inside.md")}
    got = {k: contained_read(*v) for k, v in cases.items()}
    git_sha = subprocess.run(["git", "hash-object", "--stdin"], input=body, capture_output=True).stdout.decode().strip()
    q = {"Q1": got["F1"][1] == git_sha,
         "Q2": got["F1"][1] == got["F5"][1] == got["F15"][1] and got["F1"][1] is not None,
         "Q3": contained_read(tam, "inside.md") == got["F1"]}

res = {k: got[k][0] == EXPECT[k] for k in EXPECT}
res.update(q)
print(json.dumps({"codes": {k: got[k][0] for k in sorted(got, key=lambda s: int(s[1:]))},
                  "blob_F1": got["F1"][1],
                  "predictions": {k: ("MATCH" if v else "MISS") for k, v in res.items()},
                  "matched": sum(res.values()), "of": len(res)}, sort_keys=True))
