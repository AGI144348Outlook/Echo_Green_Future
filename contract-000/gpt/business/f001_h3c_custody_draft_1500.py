#!/usr/bin/env python3
"""F-001 H3c draft: fail-closed source custody verifier, stdlib only.
NOT TESTED, NOT AUTHENTICATED, NOT RELEASE APPROVAL.
Usage: python3 f001_h3c_custody_draft_1500.py manifest.json source_directory
Manifest schema: source_commit (40 lowercase hex), files [{path,sha256,size}],
editorial_approved, rights_approved, owner_release_authorized (all literal true).
Reads source bytes only. Never publishes, uploads or modifies inputs.
"""
import hashlib, json, os, re, stat, sys
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

def hold(reason):
    print(json.dumps({"status":"HOLD","reason":reason},sort_keys=True))
    return 2

def verify(manifest_path, root):
    try:
        with open(manifest_path, "rb") as f:
            m = json.loads(f.read())
        if not isinstance(m,dict) or not HEX40.fullmatch(str(m.get("source_commit",""))):
            return hold("missing/invalid pinned source commit")
        files=m.get("files")
        if not isinstance(files,list) or not files:
            return hold("no source files")
        seen=set()
        root_fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            for entry in files:
                if not isinstance(entry,dict):
                    return hold("bad entry")
                rel=entry.get("path")
                if not isinstance(rel,str) or not rel or rel.startswith("/") or "\\" in rel:
                    return hold("unsafe path")
                parts=rel.split("/")
                if any(p in ("",".","..") for p in parts) or rel in seen:
                    return hold("unsafe or duplicate path")
                seen.add(rel)
                if not HEX64.fullmatch(str(entry.get("sha256",""))) or type(entry.get("size")) is not int or entry["size"]<0:
                    return hold("bad size/hash")
                parent=os.dup(root_fd)
                try:
                    for component in parts[:-1]:
                        child=os.open(component,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent)
                        os.close(parent);parent=child
                    fd=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent)
                    try:
                        before=os.fstat(fd)
                        if not stat.S_ISREG(before.st_mode):
                            return hold("not regular file")
                        digest=hashlib.sha256()
                        total=0
                        while True:
                            chunk=os.read(fd,65536)
                            if not chunk:break
                            total+=len(chunk);digest.update(chunk)
                        after=os.fstat(fd)
                        if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns):
                            return hold("file changed during read")
                        if total!=entry["size"] or digest.hexdigest()!=entry["sha256"]:
                            return hold("source bytes mismatch")
                    finally:os.close(fd)
                finally:os.close(parent)
        finally:os.close(root_fd)
        if not all(m.get(k) is True for k in ("editorial_approved","rights_approved","owner_release_authorized")):
            return hold("missing explicit approval evidence")
        return hold("internally consistent only; no independent authenticated custody receipt")
    except (OSError,ValueError,TypeError,KeyError,json.JSONDecodeError) as e:
        return hold("invalid input or file operation: "+type(e).__name__)

if __name__=="__main__":
    sys.exit(verify(sys.argv[1],sys.argv[2]) if len(sys.argv)==3 else hold("usage"))
