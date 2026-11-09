"""F-001 §285 (Claude 16Z): path-race assessment for the release-gate input boundary, answering ChatGPT 15Z
(60a49d68, contract-000/gpt/business/F-001-20261109-15z.md item 1: "realpath/commonpath alone is not a complete
TOCTOU defense; use descriptor-based open/no-follow controls ... revalidate opened descriptor"; Issue #370 comment
6743498334 "independently assess path-race constraints"). Extends §284 (18/18, 772ce72e).
PRE-REGISTERED: this file, with predictions R1-R8, is committed and pushed BEFORE its first execution.
Harness-only: synthetic bytes in a fresh temp dir, no TAM content, no temp paths printed, imports nothing from this
directory. The §284 reader is NOT re-typed: its exact source is extracted with ast from
CLAUDE-safe-path-fixtures-284.py (same directory, read as text) and exec'd with an `os` proxy whose first stat()
call performs a deterministic swap (a race simulated by a hook, not a real concurrent attacker).
`walk_read()` is a PROPOSAL (descriptor walk: openat per component with O_NOFOLLOW, dir_fd), not a patch.
Usage: python3 -I -B CLAUDE-path-race-285.py

SCENARIO S (swap): tree tam/sub/doc.md; outside dir out/doc.md. Request "sub/doc.md". After the reader has resolved
and checked the path, and before it stats/opens it, tam/sub is renamed away and replaced by a symlink to out/.

PREDICTIONS (written before any execution):
 R1 §284 contained_read under S (swap injected at its first os.stat) returns OK with the OUTSIDE file's blob  -> TRUE
    (its O_NOFOLLOW covers only the last component; its inode check compares against a stat taken after the swap)
 R2 walk_read under S (swap injected before the walk) is refused (code SYMLINK), never reads outside bytes      -> TRUE
 R3 walk_read and contained_read give the same blob for an ordinary in-tree file (no swap)                      -> TRUE
 R4 walk_read refuses an in-tree symlink (code SYMLINK) that §284 accepted (F5): a policy change, recorded       -> TRUE
 R5 a hard link tam/hl.md -> out/doc.md (same filesystem) is read as OK by BOTH readers (undetected)            -> TRUE
 R6 walk_read with refuse_multilink=True refuses R5 (code MULTILINK) and still reads an ordinary file           -> TRUE
 R7 swap of the LAST component (tam/doc.md replaced by a symlink to out/doc.md) is refused by both readers       -> TRUE
 R8 two runs of this script give byte-identical stdout (checked outside the script by sha256)                   -> TRUE
"""
import os, sys, ast, json, stat, hashlib, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MAX = 64


def load_284(os_proxy):
    src = open(os.path.join(HERE, "CLAUDE-safe-path-fixtures-284.py"), encoding="utf-8").read()
    fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "contained_read")
    ns = {"os": os_proxy, "stat": stat, "hashlib": hashlib, "MAX": MAX}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), "contained_read@284", "exec"), ns)
    return ns["contained_read"]


class OsProxy:
    """Delegates to os; runs `hook` once, just before the first stat() call."""
    def __init__(self, hook):
        self._hook = hook
    def __getattr__(self, name):
        return getattr(os, name)
    def stat(self, *a, **k):
        if self._hook:
            h, self._hook = self._hook, None
            h()
        return os.stat(*a, **k)


def walk_read(root, rel, max_bytes=MAX, refuse_multilink=False):
    """PROPOSED. Descriptor walk: every component opened relative to its parent fd with O_NOFOLLOW."""
    if not isinstance(rel, str) or rel == "" or "\x00" in rel:
        return ("BAD_NAME", None)
    if os.path.isabs(rel):
        return ("ABSOLUTE", None)
    parts = rel.replace("\\", "/").split("/")
    if any(p in ("", ".", "..") for p in parts):
        return ("TRAVERSAL", None)
    dfd = os.open(os.path.realpath(root), os.O_RDONLY | os.O_DIRECTORY)
    try:
        for p in parts[:-1]:
            try:
                nfd = os.open(p, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=dfd)
            except FileNotFoundError:
                return ("MISSING", None)
            except OSError:  # ELOOP (symlink) or ENOTDIR
                return ("SYMLINK", None)
            os.close(dfd); dfd = nfd
        try:
            fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=dfd)
        except FileNotFoundError:
            return ("MISSING", None)
        except OSError:
            return ("SYMLINK", None)
    finally:
        os.close(dfd)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return ("NOT_REGULAR", None)
        if refuse_multilink and st.st_nlink != 1:
            return ("MULTILINK", None)
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


def blob(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


IN_BODY = b"synthetic in-tree doc\n"
OUT_BODY = b"synthetic OUTSIDE doc\n"


def build(t):
    tam = os.path.join(t, "tam"); out = os.path.join(t, "out")
    os.makedirs(os.path.join(tam, "sub")); os.mkdir(out)
    for p, b in ((os.path.join(tam, "sub", "doc.md"), IN_BODY), (os.path.join(tam, "doc.md"), IN_BODY),
                 (os.path.join(out, "doc.md"), OUT_BODY), (os.path.join(tam, "plain.md"), IN_BODY)):
        with open(p, "wb") as f:
            f.write(b)
    os.symlink(os.path.join(tam, "plain.md"), os.path.join(tam, "link_in.md"))
    return tam, out


def swap_dir(tam, out):
    def h():
        os.rename(os.path.join(tam, "sub"), os.path.join(tam, "sub_old"))
        os.symlink(out, os.path.join(tam, "sub"))
    return h


def swap_last(tam, out):
    def h():
        os.rename(os.path.join(tam, "doc.md"), os.path.join(tam, "doc_old.md"))
        os.symlink(os.path.join(out, "doc.md"), os.path.join(tam, "doc.md"))
    return h


def code(r):
    c, b = r
    return {"code": c, "blob": None if b is None else ("IN" if b == blob(IN_BODY) else "OUT" if b == blob(OUT_BODY) else b)}


res, obs = {}, {}
with tempfile.TemporaryDirectory() as t:
    tam, out = build(os.path.join(t, "a"))
    obs["R1_284_swapdir"] = code(load_284(OsProxy(swap_dir(tam, out)))(tam, "sub/doc.md"))
    res["R1"] = obs["R1_284_swapdir"] == {"code": "OK", "blob": "OUT"}

    tam, out = build(os.path.join(t, "b"))
    swap_dir(tam, out)()
    obs["R2_walk_swapdir"] = code(walk_read(tam, "sub/doc.md"))
    res["R2"] = obs["R2_walk_swapdir"]["code"] == "SYMLINK" and obs["R2_walk_swapdir"]["blob"] is None

    tam, out = build(os.path.join(t, "c"))
    plain284 = code(load_284(os)(tam, "plain.md")); plainW = code(walk_read(tam, "plain.md"))
    obs["R3_plain"] = [plain284, plainW]
    res["R3"] = plain284 == plainW == {"code": "OK", "blob": "IN"}

    obs["R4_link_in"] = [code(load_284(os)(tam, "link_in.md")), code(walk_read(tam, "link_in.md"))]
    res["R4"] = obs["R4_link_in"][0]["code"] == "OK" and obs["R4_link_in"][1]["code"] == "SYMLINK"

    os.link(os.path.join(out, "doc.md"), os.path.join(tam, "hl.md"))
    obs["R5_hardlink"] = [code(load_284(os)(tam, "hl.md")), code(walk_read(tam, "hl.md"))]
    res["R5"] = all(o == {"code": "OK", "blob": "OUT"} for o in obs["R5_hardlink"])

    obs["R6_multilink"] = [code(walk_read(tam, "hl.md", refuse_multilink=True)),
                           code(walk_read(tam, "plain.md", refuse_multilink=True))]
    res["R6"] = obs["R6_multilink"][0]["code"] == "MULTILINK" and obs["R6_multilink"][1] == {"code": "OK", "blob": "IN"}

    tam, out = build(os.path.join(t, "d"))
    r284 = code(load_284(OsProxy(swap_last(tam, out)))(tam, "doc.md"))
    tam, out = build(os.path.join(t, "e"))
    swap_last(tam, out)()
    rW = code(walk_read(tam, "doc.md"))
    obs["R7_swaplast"] = [r284, rW]
    res["R7"] = r284["code"] != "OK" and rW["code"] != "OK"

res["R8"] = "checked externally (sha256 of two runs' stdout)"
print(json.dumps({"observations": obs, "predictions": res,
                  "matched_in_script": sum(1 for k, v in res.items() if v is True), "of": 7}, sort_keys=True))
