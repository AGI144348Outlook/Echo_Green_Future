#!/usr/bin/env python3
"""F-001 HOLD-only editorial occurrence/evidence manifest schema check.

Usage: python3 -I f001_occurrence_evidence_gate_392.py QUEUE.json DECISIONS.json
Read-only: no publication or truth/rights verification. Every result stays HOLD.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HEX64 = re.compile(r'^[0-9a-f]{64}$')
ACTIONS = {'retain_claimed', 'retain_sourced', 'qualify', 'cut'}

def check(queue, manifest):
    errors = []
    cards = queue.get('cards', [])
    ids = [c.get('id') for c in cards]
    if queue.get('project') != 'F-001' or manifest.get('project') != 'F-001':
        errors.append('project must be F-001 in both inputs')
    if len(cards) != queue.get('card_count') or len(set(ids)) != len(ids) or any(not i for i in ids):
        errors.append('queue card count/IDs invalid')
    for card in cards:
        if not all(card.get(k) for k in ('source_file', 'source_blob_sha', 'full_sentence')):
            errors.append(f'queue source binding missing: {card.get("id")}')
    by_id = {c.get('id'): c for c in cards}
    decisions = manifest.get('decisions', [])
    evidence = manifest.get('evidence', [])
    receipts = manifest.get('artifact_receipts', [])
    dcounts = Counter(d.get('occurrence_id') for d in decisions)
    ecounts = Counter(e.get('id') for e in evidence)
    if any(n != 1 for n in dcounts.values()):
        errors.append('duplicate decision occurrence ID')
    if any(n != 1 for n in ecounts.values()):
        errors.append('duplicate evidence ID')
    if any(i not in by_id for i in dcounts):
        errors.append('decision references unknown occurrence')
    ev = {e.get('id'): e for e in evidence}
    for d in decisions:
        ident = d.get('occurrence_id')
        if ident not in by_id:
            continue
        action = d.get('action')
        if action not in ACTIONS:
            errors.append(f'{ident}: invalid action')
            continue
        if not d.get('reviewer') or not d.get('editorial_note'):
            errors.append(f'{ident}: reviewer and editorial note required')
        if action != 'cut' and (d.get('rights') != 'cleared' or not d.get('rights_basis')):
            errors.append(f'{ident}: retained text needs rights clearance and basis')
        if action == 'qualify' and not d.get('replacement_text'):
            errors.append(f'{ident}: qualifying text missing')
        if action == 'retain_sourced':
            refs = d.get('evidence_refs') or []
            if not refs:
                errors.append(f'{ident}: sourced claim lacks evidence reference')
            for ref in refs:
                e = ev.get(ref)
                if not e or e.get('occurrence_id') != ident or not all(e.get(k) for k in ('reference', 'locator', 'reviewed_by')):
                    errors.append(f'{ident}: evidence reference not independently occurrence-bound: {ref}')
        if action == 'cut':
            for fmt in ('epub', 'pdf'):
                hits = [a for a in receipts if a.get('occurrence_id') == ident and a.get('format') == fmt]
                if len(hits) != 1 or hits[0].get('absent') is not True or not HEX64.fullmatch(str(hits[0].get('artifact_sha256', ''))):
                    errors.append(f'{ident}: missing/invalid {fmt} cut-absence receipt')
    decided = len([i for i in dcounts if i in by_id])
    return {
        'project': 'F-001',
        'release_status': 'HOLD',
        'release_authorized': False,
        'schema_complete': not errors and decided == len(cards) and len(cards) > 0,
        'card_count': len(cards),
        'decided_occurrences': decided,
        'pending_occurrences': len(cards) - decided,
        'errors': errors,
        'limitations': 'Schema/attestation only; no independent evidence, rights, EPUB/PDF bytes, citations, or publication verified.'
    }

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    queue = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    manifest = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
    result = check(queue, manifest)
    print(json.dumps(result, indent=2))
    sys.exit(1 if result['errors'] else 0)
