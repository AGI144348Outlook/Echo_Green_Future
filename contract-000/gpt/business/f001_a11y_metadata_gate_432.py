#!/usr/bin/env python3
"""F-001 HOLD-only EPUB metadata preflight. Not an EPUBCheck/Ace or release approval.

Checks a bounded EPUB ZIP, a single container-selected OPF, parseable package
XML, and nonduplicated accessibility property/value pairs. Fails closed.
Usage: python3 -I -B f001_a11y_metadata_gate_432.py <epub>
"""
import json
import posixpath
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

MAX_ARCHIVE = 64 * 1024 * 1024
MAX_MEMBERS = 2048
MAX_XML = 2 * 1024 * 1024
A11Y = {"accessMode", "accessModeSufficient", "accessibilityFeature",
        "accessibilityHazard", "accessibilitySummary", "accessibilityAPI",
        "accessibilityControl", "certifiedBy", "certifierCredential"}


def local(tag):
    return tag.rsplit('}', 1)[-1]


def inspect(path):
    errors = []
    metadata = []
    p = Path(path)
    try:
        bad_file = p.is_symlink() or not p.is_file() or p.stat().st_size > MAX_ARCHIVE
    except OSError:
        bad_file = True
    if bad_file:
        return {"ok": False, "errors": ["invalid_or_oversized_archive"], "metadata_pairs": 0}
    try:
        with zipfile.ZipFile(p) as z:
            infos = z.infolist()
            names = [i.filename for i in infos]
            if len(infos) > MAX_MEMBERS or len(names) != len(set(names)):
                errors.append("member_count_or_duplicate_name")
            if not infos or infos[0].filename != 'mimetype' or infos[0].compress_type != zipfile.ZIP_STORED:
                errors.append("mimetype_not_first_and_stored")
            if ('mimetype' not in names or z.getinfo('mimetype').file_size > 64 or
                z.read('mimetype') != b'application/epub+zip'):
                errors.append("invalid_mimetype")
            if 'META-INF/container.xml' not in names:
                errors.append("missing_container")
            else:
                ci = z.getinfo('META-INF/container.xml')
                if ci.file_size > MAX_XML:
                    errors.append("oversized_container")
                else:
                    root = ET.fromstring(z.read(ci))
                    paths = [e.attrib.get('full-path') for e in root.iter() if local(e.tag) == 'rootfile']
                    if len(paths) != 1 or not paths[0]:
                        errors.append("container_rootfile_count")
                    else:
                        target = paths[0]
                        if (target.startswith('/') or '\\' in target or
                            posixpath.normpath(target) != target or target.startswith('../')):
                            errors.append("unsafe_rootfile_path")
                        opfs = [n for n in names if n.endswith('.opf')]
                        if len(opfs) != 1 or opfs[0] != target:
                            errors.append("opf_count_or_target_mismatch")
                        else:
                            oi = z.getinfo(target)
                            if oi.file_size > MAX_XML:
                                errors.append("oversized_opf")
                            else:
                                pkg = ET.fromstring(z.read(oi))
                                if local(pkg.tag) != 'package':
                                    errors.append("not_opf_package")
                                for node in pkg.iter():
                                    if local(node.tag) != 'meta':
                                        continue
                                    prop = node.attrib.get('property', '')
                                    if prop.startswith('schema:'):
                                        metadata.append((prop, ''.join(node.itertext()).strip()))
                                if not any(prop.split(':', 1)[-1] in A11Y for prop, _ in metadata):
                                    errors.append("missing_a11y_metadata")
                                dup = sorted({prop for (prop, val), count in Counter(metadata).items() if count > 1})
                                if dup:
                                    errors.append("duplicate_a11y_property_value:" + ','.join(dup))
    except (OSError, zipfile.BadZipFile, RuntimeError, ValueError, ET.ParseError, KeyError, EOFError, NotImplementedError) as e:
        errors.append("invalid_zip_or_xml:" + type(e).__name__)
    return {"ok": not errors, "errors": errors, "metadata_pairs": len(metadata)}


def main(argv):
    if len(argv) != 2:
        print('usage: f001_a11y_metadata_gate_432.py <epub>', file=sys.stderr)
        return 2
    result = inspect(argv[1])
    result.update({"project": "F-001", "release": "HOLD", "publication_authorization": "ABSENT"})
    print(json.dumps(result, sort_keys=True))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
