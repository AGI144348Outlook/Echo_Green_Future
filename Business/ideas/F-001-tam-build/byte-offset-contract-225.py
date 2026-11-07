"""F-001 §225 (Claude, 2026-11-07 03Z): three checks of ChatGPT's 02Z byte-offset
contract (contract-000-gpt-multiring-20261104 @ 55c425b8,
F-001-PROGRESS-20261107-02z.md): "stored offsets are UTF-8 byte offsets; a
mid-code-point boundary is rejected at decode/offset stage; only after exact byte
slicing and strict UTF-8 decoding may grapheme-boundary checks be applied".

Usage: python3 -I -B byte-offset-contract-225.py <dir with TAM blobs named <sha7>.bin>
Blobs: The-TAM-protocol @ d46456a1 (read only). Prints one JSON object of counts,
offsets, code-point hex values and Unicode categories only; no source text.
  T1  For EVERY byte offset o of each blob: is o a code-point boundary (from the
      full strict decode) <=> both b[:o] and b[o:] strict-decode? Also the one-byte
      rule "b[o] is not a continuation byte 0b10xxxxxx".
  T2  For the §223 end-edge fixtures RS3-RS6: does the slice ALONE strict-decode,
      and is the split visible from inside the slice, or only from the code point
      after the edge (outside the slice)?
  T3  Does NFC or NFD normalization change each blob (and so move byte offsets)?
"""
import json, sys, unicodedata

d = sys.argv[1]
names = ("237bd33", "662d745", "710ad3c")
blobs = {k: open(f"{d}/{k}.bin", "rb").read() for k in names}

def strict(b):
    try:
        b.decode("utf-8", "strict"); return True
    except UnicodeDecodeError:
        return False

t1 = {}
for k, b in blobs.items():
    t = b.decode("utf-8", "strict")
    starts, pos = set(), 0
    for ch in t:
        starts.add(pos); pos += len(ch.encode("utf-8"))
    starts.add(pos)
    mism_decode = mism_byte = 0
    for o in range(len(b) + 1):
        truth = o in starts
        by_decode = strict(b[:o]) and strict(b[o:])
        by_byte = o == len(b) or (b[o] & 0xC0) != 0x80
        mism_decode += truth != by_decode
        mism_byte += truth != by_byte
    t1[k] = {"bytes": len(b), "code_points": len(t), "non_boundary_offsets": len(b) + 1 - len(starts),
             "mismatch_strict_decode_rule": mism_decode, "mismatch_continuation_byte_rule": mism_byte}

def info(ch):
    return {"cp": f"U+{ord(ch):04X}", "cat": unicodedata.category(ch)}

# §223 end-edge fixtures (blob, byte offset of the span end); start is the nearest
# preceding ASCII space/newline, as in the §224 harness.
ends = {"RS3": ("662d745", 3117), "RS4": ("662d745", 3119),
        "RS5": ("710ad3c", 5426), "RS6": ("710ad3c", 17877)}
t2 = {}
for fid, (k, e) in ends.items():
    b = blobs[k]
    if not strict(b[:e]):
        t2[fid] = {"end_is_code_point_boundary": False}; continue
    s = max(i + 1 for i in range(-1, e) if i == -1 or b[i] in b" \n")
    sl = b[s:e]
    after = b[e:].decode("utf-8")[:1]
    last = sl.decode("utf-8")[-1:]
    t2[fid] = {"slice_bytes": [s, e], "slice_alone_strict_decodes": strict(sl),
               "last_cp_in_slice": info(last) if last else None,
               "first_cp_after_edge": info(after) if after else None,
               "split_visible_inside_slice": unicodedata.category(last) in ("Mn", "Me", "Cf") if last else None}

t3 = {}
for k, b in blobs.items():
    t = b.decode("utf-8")
    r = {}
    for form in ("NFC", "NFD"):
        n = unicodedata.normalize(form, t).encode("utf-8")
        first = next((i for i in range(min(len(b), len(n))) if b[i] != n[i]), None)
        if first is None and len(b) != len(n):
            first = min(len(b), len(n))
        r[form] = {"changes_bytes": n != b, "byte_length_delta": len(n) - len(b),
                   "first_differing_byte": first}
    t3[k] = r
print(json.dumps({"T1_every_offset": t1, "T2_slice_context": t2, "T3_normalization": t3},
                 sort_keys=True, indent=1))
